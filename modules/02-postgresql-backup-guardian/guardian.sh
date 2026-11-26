#!/usr/bin/env bash
# PostgreSQL Backup Guardian — sauvegardes logiques locales.
set -Eeuo pipefail
umask 077
export PATH=/usr/sbin:/usr/bin:/sbin:/bin
unset PGHOST PGHOSTADDR PGPORT PGUSER PGDATABASE PGSERVICE PGSERVICEFILE PGOPTIONS PGCLUSTER PGPASSWORD PGCLIENTENCODING
VERSION=1.0.0
fail(){ printf 'Erreur : %s\n' "$*" >&2; exit 1; }
log(){ printf '%s %s\n' "$(date -Is)" "$*" >&2; }
need(){ command -v "$1" >/dev/null || fail "Commande absente : $1"; }
ident(){ [[ $1 =~ ^[a-zA-Z_][a-zA-Z0-9_]{0,62}$ ]] || fail "Identifiant non pris en charge : $1"; }
number(){ [[ $1 =~ ^[1-9][0-9]{0,3}$ ]] || fail 'Nombre entier attendu (1–9999).'; }
# Répertoire privé, sans liens symboliques dans le chemin.
private_dir(){
 [[ $1 = /* && $1 != / && $1 != *$'\n'* ]] || fail 'Chemin absolu requis.'
 [[ $(realpath -e -- "$1") == "$1" && -d $1 ]] || fail 'Répertoire existant, canonique et sans lien requis.'
 [[ $(stat -c '%u:%a' -- "$1") == "$(id -u):700" ]] || fail 'Répertoire propriétaire courant, mode 0700 requis.'
}
# Sélection explicite du cluster Debian/Ubuntu et de son port.
cluster(){
 local v=$1 c=$2 line status
 [[ $v =~ ^[0-9]+$ && $c =~ ^[a-zA-Z0-9_][a-zA-Z0-9_-]*$ ]] || fail 'Cluster invalide.'
 need pg_lsclusters
 line=$(pg_lsclusters --no-header | awk -v v="$v" -v c="$c" '$1==v && $2==c {print $3, $4}')
 [[ -n $line && $line != *$'\n'* ]] || fail 'Cluster introuvable ou ambigu.'
 read -r PORT status <<< "$line"
 [[ $PORT =~ ^[0-9]+$ && $status == online* ]] || fail 'Cluster hors ligne.'
 BIN=/usr/lib/postgresql/$v/bin
 [[ -x $BIN/pg_dump && -x $BIN/psql && -x $BIN/pg_restore ]] || fail 'Binaires PostgreSQL absents.'
 # Authentification locale peer : exécution sous postgres uniquement.
 [[ $(id -un) == postgres ]] || fail 'Exécuter sous postgres (sudo -u postgres).'
 CONN=(-h /var/run/postgresql -p "$PORT" -U postgres -w)
 "$BIN/psql" "${CONN[@]}" -X -At -d postgres -v ON_ERROR_STOP=1 -c 'SELECT 1' >/dev/null
}
# Chaque sauvegarde est publiée atomiquement dans un dossier autonome.
backup(){
 [[ $# == 4 ]] || fail 'backup VERSION CLUSTER BASE REPERTOIRE'
 local v=$1 c=$2 db=$3 root=$4 stamp tmp dest
 ident "$db"; cluster "$v" "$c"; private_dir "$root"
 exec 9>"$root/.guardian.lock"; flock -n 9 || fail 'Opération concurrente.'
 stamp=$(date -u +%Y%m%dT%H%M%SZ); dest="$root/${v}_${c}_${db}_${stamp}"
 [[ ! -e $dest ]] || fail 'Destination déjà présente.'
 tmp=$(mktemp -d "$root/.pending.XXXXXXXX")
 trap "rm -rf -- $(printf '%q' "$tmp")" EXIT
 log "Sauvegarde de $db sur $v/$c"
 "$BIN/pg_dump" "${CONN[@]}" -Fc --dbname="$db" --file="$tmp/database.dump"
 "$BIN/pg_restore" --list "$tmp/database.dump" > "$tmp/catalogue.txt"
 # Les rôles sont sensibles : export séparé sans mots de passe.
 "$BIN/pg_dumpall" "${CONN[@]}" --globals-only --no-role-passwords --file="$tmp/globals.sql"
 printf 'version=%s\ncluster=%s\nport=%s\ndatabase=%s\ncreated_utc=%s\n' "$v" "$c" "$PORT" "$db" "$stamp" > "$tmp/manifest.txt"
 (cd "$tmp"; sha256sum database.dump catalogue.txt globals.sql manifest.txt > SHA256SUMS)
 mv -T -- "$tmp" "$dest"; trap - EXIT
 log 'Sauvegarde publiée.'; printf '%s\n' "$dest"
}
verify(){
 [[ $# == 1 ]] || fail 'verify DOSSIER'
 private_dir "$1"
 local f
 for f in database.dump catalogue.txt globals.sql manifest.txt SHA256SUMS; do [[ -f $1/$f && ! -L $1/$f ]] || fail "Fichier manquant : $f"; done
 # Ne jamais suivre des chemins arbitraires fournis par le manifeste.
 (cd "$1"; sha256sum database.dump catalogue.txt globals.sql manifest.txt | cmp - SHA256SUMS) || fail 'Sommes SHA-256 différentes.'
 log 'Intégrité SHA-256 vérifiée.'
}
restore(){
 [[ $# == 4 ]] || fail 'restore VERSION CLUSTER DOSSIER NOUVELLE_BASE'
 local v=$1 c=$2 archive=$3 target=$4
 ident "$target"; [[ $target == guardian_restore_* ]] || fail 'Préfixe guardian_restore_ obligatoire.'
 cluster "$v" "$c"; verify "$archive"
 "$BIN/pg_restore" --list "$archive/database.dump" >/dev/null
 # createdb refuse une base existante : aucun écrasement.
 "$BIN/createdb" "${CONN[@]}" -T template0 "$target"
 if ! "$BIN/pg_restore" "${CONN[@]}" --exit-on-error --single-transaction --no-owner --no-privileges -d "$target" "$archive/database.dump"; then
  fail "Restauration échouée ; base $target conservée pour diagnostic."
 fi
 "$BIN/psql" "${CONN[@]}" -X -d "$target" -v ON_ERROR_STOP=1 -c "SELECT schemaname,count(*) AS tables FROM pg_tables WHERE schemaname NOT IN ('pg_catalog','information_schema') GROUP BY 1 ORDER BY 1;"
 log "Restauration terminée : $target (validation métier encore nécessaire)."
}
# Inventaire et simulation de rétention ; suppression jamais automatique ici.
retention(){
 [[ $# == 2 ]] || fail 'retention-plan REPERTOIRE JOURS'
 private_dir "$1"; number "$2"
 find "$1" -mindepth 1 -maxdepth 1 -type d -name '[0-9]*_*_*_????????T??????Z' -mtime "+$2" -print
 log 'Simulation uniquement : aucun fichier supprimé.'
}
list(){ [[ $# == 1 ]] || fail 'list REPERTOIRE'; private_dir "$1"; find "$1" -mindepth 2 -maxdepth 2 -name manifest.txt -type f -print; }
help(){ cat <<'HELP'
PostgreSQL Backup Guardian 1.0.0
  clusters
  backup VERSION CLUSTER BASE REPERTOIRE
  verify DOSSIER
  restore VERSION CLUSTER DOSSIER guardian_restore_NOM
  list REPERTOIRE
  retention-plan REPERTOIRE JOURS
  interactive
  --version | --help
Exécuter les sauvegardes et restaurations sous postgres.
HELP
}
menu(){
 local choice v c db dir target days
 while true; do
 printf '\n=== BACKUP GUARDIAN ===\n1. Clusters\n2. Sauvegarder\n3. Vérifier\n4. Restaurer (nouvelle base)\n5. Inventaire\n6. Simulation rétention\n0. Quitter\n'
 read -rp 'Choix : ' choice || return 0
 case $choice in
 1) pg_lsclusters;;
 2) read -rp 'Version : ' v; read -rp 'Cluster : ' c; read -rp 'Base : ' db; read -rp 'Répertoire : ' dir; bash "${BASH_SOURCE[0]}" backup "$v" "$c" "$db" "$dir" || log 'Échec';;
 3) read -rp 'Dossier : ' dir; bash "${BASH_SOURCE[0]}" verify "$dir" || log 'Échec';;
 4) read -rp 'Version : ' v; read -rp 'Cluster : ' c; read -rp 'Dossier : ' dir; read -rp 'Nouvelle base guardian_restore_... : ' target; bash "${BASH_SOURCE[0]}" restore "$v" "$c" "$dir" "$target" || log 'Échec';;
 5) read -rp 'Répertoire : ' dir; bash "${BASH_SOURCE[0]}" list "$dir" || log 'Échec';;
 6) read -rp 'Répertoire : ' dir; read -rp 'Jours : ' days; bash "${BASH_SOURCE[0]}" retention-plan "$dir" "$days" || log 'Échec';;
 0) return 0;; *) log 'Choix invalide';;
 esac; done
}
# Un processus enfant conserve errexit même lorsque le menu gère un échec.
if [[ ${1:-} == interactive || $# == 0 ]]; then
 # Le menu appelle des commandes indépendantes pour éviter errexit conditionnel.
 menu; exit
fi
cmd=$1; shift
case $cmd in
 backup) backup "$@";; verify) verify "$@";; restore) restore "$@";; list) list "$@";; retention-plan) retention "$@";; clusters) pg_lsclusters;; --version) echo "$VERSION";; --help|-h) help;; *) fail 'Commande inconnue';;
esac
