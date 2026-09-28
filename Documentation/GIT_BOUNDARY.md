# Git and Local-Data Boundary

`Codebase` is the sole active product Git root. A public clone must contain
only public-safe software and documentation. `Academic World` is a sibling
local-only data world and never belongs in a commit.

## Allowed outer-repository material

- Studies-owned source code, tests, schemas, migrations, launchers, and tools.
- Public-safe documentation and the authoritative master plan.
- Synthetic fixtures and examples that contain no real account, course, file,
  grade, attendance, correspondence, or university evidence.

## Excluded material

- Every file in `Academic World`.
- Runtime credentials, site configuration, databases, Docker/Bench state,
  logs, downloads, backups, indexes, mail archives, and local manifests.
- Local vendor working trees, which are documented but intentionally not
  embedded in the outer Git repository.

## Nested-repository policy

The Frappe, Frappe Learning, Frappe Docker, and Payments checkouts are
intentional local vendor repositories. Owned legacy repositories are backed up
as local Git bundles before their active nested metadata is removed and their
reviewed source is incorporated into this outer repository.

Run the staged-content privacy review before every push. A suspicious file is
not staged until it is proven public-safe; uncertainty always keeps it local.
