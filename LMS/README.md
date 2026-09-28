# LMS control workspace

This is the local Studies continuity workspace for orchestration, Windows setup,
and runtime documentation. The outer `Codebase` repository owns the public-safe
Studies code; upstream vendor checkouts and local runtime state remain excluded
from that repository.

## Repositories

- `frappe-lms/` — canonical upstream Frappe Learning checkout at `v2.63.0`; it is a documented vendor checkout and is excluded from the outer repository.
- `studies_hub/` — the Studies Hub app, installed beside Frappe Learning and tracked by the outer repository after reconciliation.
- `frappe_docker/` — clean official development-reference checkout, retained locally as vendor source.
- `../Our_Bridge_For_Windows_Files/` — the independent local-file bridge, tracked by the outer repository after reconciliation.
- `scripts/` and `runtime/` — Windows setup/launch orchestration and the project-owned local development stack.

## Runtime boundary

The Compose stack uses Frappe's documented development workflow with Frappe Framework `version-16`, Frappe Learning `v2.63.0`, MariaDB, and Redis. `runtime/bench/` contains durable local runtime files and site uploads; MariaDB persists in a Docker named volume. Neither is a canonical Academic World. The legacy vault is mounted from `Academic World/_Migration Inbox/Academic Vault Legacy/`; personal study data remains outside container mounts. The Bench app path soft-links to the `studies_hub/` worktree so the installed app path remains unchanged.

See [runtime/README.md](runtime/README.md) for setup, recovery, and data boundaries. `Launch Studies.cmd` starts the local environment after provisioning.
