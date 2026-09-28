# Local runtime

This directory contains the project-owned Docker Compose development stack. It follows Frappe's documented development workflow: Bench on the `version-16` branch, MariaDB, and separate Redis cache and queue services. The Frappe Learning source is pinned to the preserved canonical checkout at `v2.63.0`; Studies Hub remains a separate app repository.

## Durable data boundaries

- `bench/` is a host-visible working runtime for Bench, site files, and uploads. It can be rebuilt only through explicit operator action; scripts never remove or reset it.
- MariaDB uses the persistent Docker volume `studies_mariadb-data`. Never use `docker compose down -v` or remove this volume.
- `../../../Academic World/_Migration Inbox/Academic Vault Legacy/` from this runtime directory is the currently preserved visible academic vault, mounted at `/workspace/academic-vault`. It is local-only and excluded from Git until its university/course mapping is explicitly reviewed.
- `Academic World/Personal Study/` is user-authored/personal study material. It is not mounted into containers and is not a runtime directory.
- `.env` contains local DB and site-admin credentials, is ignored, and is created once by `Initialize-StudiesRuntime.ps1`. That script preserves an existing file. Do not commit or share it.
- `logs/` and `bench/bench.log` contain local diagnostics.

## Setup and launch

The launcher resolves the Studies root relative to its own location, so the
project can be moved without a hard-coded Desktop path. From PowerShell,
initialize or resume the local runtime from the script's current location:

```powershell
& (Join-Path $PSScriptRoot '..\scripts\Initialize-StudiesRuntime.ps1')
```

The script validates Compose, starts local services, initializes Bench, installs payments and Frappe Learning, then soft-links the read-only `studies_hub/` worktree so uncommitted development files are visible to the site. It creates the synthetic test course and visible vault files, then starts Bench and checks the local LMS endpoint. It is resumable: it never drops a database, deletes site files, or overwrites an existing local `.env`. A prior cloned Studies Hub checkout is retained under a backup name before the soft-link is created. If a partial Bench or site directory is detected, it stops and preserves the files for inspection. Studies Hub remains separate from upstream `lms`; Frappe Learning core remains unchanged.

Future launches use `Launch Studies.cmd` in the project root.

To inspect logs without changing state:

```powershell
$runtime = $PSScriptRoot
docker compose --project-directory $runtime --env-file (Join-Path $runtime '.env') -f (Join-Path $runtime 'compose.yaml') logs --tail 200
```

The synthetic course and simulated source records are local test data. No real Moodle, Teams, APSpace, or university authentication is performed.
