#!/usr/bin/env bash
set -Eeuo pipefail

BENCH_DIR=/workspace/development/frappe-bench
SITE_NAME="${SITE_NAME:-studies.localhost}"
STUDIES_HUB_VAULT_ROOT="${STUDIES_HUB_VAULT_ROOT:-/workspace/academic-vault}"
: "${MARIADB_ROOT_PASSWORD:?Missing MARIADB_ROOT_PASSWORD}"
: "${SITE_ADMIN_PASSWORD:?Missing SITE_ADMIN_PASSWORD}"
mkdir -p "$STUDIES_HUB_VAULT_ROOT"

if [[ ! -d "$BENCH_DIR/apps/frappe" ]]; then
    if [[ -e "$BENCH_DIR" ]] && find "$BENCH_DIR" -mindepth 1 -maxdepth 1 -print -quit | grep -q .; then
        echo "Bench directory exists but is incomplete; preserving it for inspection: $BENCH_DIR" >&2
        exit 20
    fi
    bench init --skip-redis-config-generation --frappe-branch version-16 "$BENCH_DIR"
fi

cd "$BENCH_DIR"
bench set-config -g db_host mariadb
bench set-config -g redis_cache redis://redis-cache:6379
bench set-config -g redis_queue redis://redis-queue:6379
bench set-config -g redis_socketio redis://redis-queue:6379

# Windows-mounted repositories can appear owned by a different UID inside
# the container. Trust only these project-owned, read-only source checkouts.
for mounted_repo in /workspace/project/frappe-lms /workspace/project/studies_hub; do
    safe_path="$mounted_repo"
    if ! git config --global --get-all safe.directory | grep -Fxq "$safe_path"; then
        git config --global --add safe.directory "$safe_path"
    fi
done

if [[ ! -d apps/payments ]]; then
    bench get-app --branch version-16 payments https://github.com/frappe/payments
fi
if [[ ! -d apps/lms ]]; then
    bench get-app --branch v2.63.0 /workspace/project/frappe-lms
fi
if [[ -L apps/studies_hub ]]; then
    linked_app="$(readlink -f apps/studies_hub)"
    if [[ "$linked_app" != /workspace/project/studies_hub ]]; then
        echo "Studies Hub link points somewhere unexpected; preserving it for inspection: $linked_app" >&2
        exit 22
    fi
elif [[ -e apps/studies_hub ]]; then
    backup_dir="$BENCH_DIR/archived/apps/studies_hub-cloned-checkout"
    if [[ -e "$backup_dir" ]]; then
        echo "Studies Hub checkout exists and backup path is occupied; preserving both: $backup_dir" >&2
        exit 23
    fi
    mkdir -p "$(dirname "$backup_dir")"
    mv apps/studies_hub "$backup_dir"
    bench get-app --soft-link /workspace/project/studies_hub
else
    bench get-app --soft-link /workspace/project/studies_hub
fi

site_config="$BENCH_DIR/sites/$SITE_NAME/site_config.json"
site_dir="$BENCH_DIR/sites/$SITE_NAME"
if [[ ! -f "$site_config" ]]; then
    if [[ -e "$site_dir" ]]; then
        echo "Site directory exists without site_config.json; preserving it for inspection: $site_dir" >&2
        exit 21
    fi
    bench new-site "$SITE_NAME" \
        --db-root-password "$MARIADB_ROOT_PASSWORD" \
        --admin-password "$SITE_ADMIN_PASSWORD" \
        --mariadb-user-host-login-scope='%'
fi

bench use "$SITE_NAME"
for app in payments lms studies_hub; do
    if ! bench --site "$SITE_NAME" list-apps | grep -Fxq "$app"; then
        bench --site "$SITE_NAME" install-app "$app"
    fi
done

bench --site "$SITE_NAME" migrate
bench --site "$SITE_NAME" execute studies_hub.academic.seed_demo.seed_demo_data
bench --site "$SITE_NAME" clear-cache
echo "Runtime initialized for $SITE_NAME. Start it with Launch Studies.cmd."
