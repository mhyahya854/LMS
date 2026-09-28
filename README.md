# Studies Codebase

This is the only Git repository for Studies. It contains public-safe software,
launchers, tests, schemas, migration tooling, and documentation.

`Academic World` is a sibling directory owned by the user. It contains local
academic information, preserved originals, private reports, backups, runtime
credentials, and other non-public material. It is physically outside this Git
root and explicitly protected by `.gitignore` as a second line of defence.

## Current layout

- `LMS/` — continuity workspace for the existing Frappe-based prototype.
- `Our_Bridge_For_Windows_Files/` — local-file bridge source.
- `Launchers/Windows/` — authoritative Windows launcher source.
- `Documentation/` — public-safe architecture and boundary documentation.
- `Vendor/` — local upstream checkouts retained for continuity and excluded
  from the outer repository; see `Documentation/VENDOR_SOURCES.md`.

The root-level `Launch Studies.cmd` delegates to
`Launchers/Windows/Launch Studies.cmd`. Both resolve the Studies root at
runtime rather than relying on a fixed Desktop path.

Before any push, inspect `git status`, `git diff --cached`, and `git ls-files`.
Never add material from `Academic World`, local runtime state, secrets, mail,
databases, logs, or real university data.
