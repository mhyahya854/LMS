# Studies Hub

This is a separate Frappe app kept outside the Frappe Learning repository. Install it beside `lms` on the Frappe v16 site. It owns the canonical academic records and local-file references; it does not patch Frappe Learning.

## Initial domain boundary

- `Canonical Course` owns stable UUID identity, preferred title, institution, program, and term.
- `External Course Mapping` links a source system and external course ID to one canonical course; `(source_system, external_course_id)` is unique.
- `Course Section` provides the local course hierarchy.
- `Academic Resource` stores provenance and keeps personal notes separate from source-derived items.
- `Academic File` points to a collision-safe, content-addressed vault path, original filename, SHA-256, size, and owning course/resource.
- `Academic Assignment` stores a due time with its timezone and source metadata.
- Desk page `/app/studies` presents local courses, source mappings, files, deadlines, and personal notes.

Keep source-derived and personal records distinguishable. Source IDs and official titles are separate from canonical titles. Store paths relative to `STUDIES_HUB_VAULT_ROOT` (the Windows runtime currently mounts the preserved legacy vault at `Academic World/_Migration Inbox/Academic Vault Legacy/` as `/workspace/academic-vault`). Files are never overwritten: their path includes SHA-256 and a sanitized filename, while the original filename is retained in metadata.

The bootstrap seeds one clearly synthetic `Computer Systems` course with three simulated source identities, Lecture 01 files, an assignment, an attendance example, and a separate personal note. It does not contact external services. `/app/studies` uses only local Frappe records; opening a file is served from the mounted vault.

Vault imports stream from disk and use SHA-256 paths. The prototype browser-open endpoint is limited to 32 MiB because Frappe's download response holds file bytes in memory; large recordings remain available in the visible Windows vault but need a streaming/range endpoint before browser playback is supported.

Run the app's pure local checks from this repository with `python -m unittest discover -s studies_hub/tests`. Run Frappe database checks after the local site exists with `bench --site studies.localhost run-tests --app studies_hub`.

## Runtime contract

Target the Frappe v16 line used by the current official LMS development guidance. Do not import or patch Frappe Learning internals for the canonical model. Do not start real Moodle/Teams/APSpace authentication until the local `Computer Systems` test course passes offline checks.
