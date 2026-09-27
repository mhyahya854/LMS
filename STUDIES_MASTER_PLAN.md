# Studies — Master Plan

Status: authoritative draft — pending owner/ChatGPT review

Scope: lifetime product direction, authority boundaries, data contract, safety
requirements, evaluation gates, and implementation sequencing. This draft is a
planning artifact only. It authorizes no source import, runtime migration,
connector, university synchronization, account authorization, or application
implementation.

This is the one primary master plan for Studies. Review cycles update this file
in place; they must reconcile affected sections rather than append a competing
plan.

## 1. Document purpose, evidence standard, and decision vocabulary

Studies is intended to be a lifelong, local-first academic system. It must
remain useful when a university account closes, an institution changes its
portal, a third-party service disappears, an AI system is unavailable, or a
database/index must be rebuilt. The product is not a folder tree, not a
Frappe site, not a university mirror, and not Hermes. It is a deterministic
academic system with a complete native application and a user-owned Academic
World.

This plan uses the following terms precisely:

- **HARD REQUIREMENT** — a behavior or constraint that a future product must
  satisfy unless the owner deliberately amends this plan.
- **FROZEN DECISION** — an owner-approved direction that implementation may
  refine technically but must not weaken for convenience. This initial draft
  deliberately contains only the frozen decisions explicitly approved by the
  owner; unresolved implementation choices are not falsely frozen.
- **PROPOSED DESIGN** — a coherent starting mechanism that implementation
  must validate before it becomes a frozen decision.
- **FUTURE INVESTIGATION** — evidence-gathering required to select a
  technical mechanism without guessing.
- **DEFERRED DECISION** — a material choice that remains open and must be
  resolved at a named gate before dependent work begins.
- **CANONICAL DATA** — durable user-owned academic truth, preserved original
  evidence, stable relationships, provenance, review decisions, and history
  required to recover or explain that truth.
- **DERIVED DATA** — data that can be regenerated from canonical data,
  including databases, indexes, search state, previews, thumbnails, caches,
  materialized views, and generated reports.
- **SOURCE OBSERVATION** — a time-bounded statement about what one source
  exposed. It is not automatically a canonical academic fact.
- **PERSONAL DATA OR NOTE** — user-authored material whose origin and sharing
  policy are independent of a university source.
- **TEST DATA** — synthetic fixture material that must never be confused with
  real academic evidence.

### 1.1 Evidence baseline for this draft

The following has been independently inspected and is used as evidence, not
as an instruction to preserve the prototype forever:

| Area | Current evidence | Confidence and limit |
|---|---|---|
| Local slice | A local synthetic Studies Hub course, simulated APSpace/Moodle/Teams mappings, local resources, deadline, provenance, personal-note separation, and offline proof were browser-verified. | **VERIFIED** only for the synthetic local slice. It is not a university integration. |
| Migration | The experimental project root was moved non-destructively; inventories, hashes, Git state, logical Frappe backup, Compose mounts, tests, and browser checks were recorded. Docker-managed MariaDB state was deliberately not copied as a folder. | **VERIFIED** experimental migration evidence. It does not choose the long-term runtime. |
| Source discovery | Read-only browser inspection produced local metadata observations and one legitimate manual Teams/SharePoint file download with an offline-open/hash check. | **VERIFIED** as a manual, inbound proof only. No automatic sync, API response, source cursor, or source merge was proven. |
| Moodle and Graph | Official protocol documentation identifies conditional future paths after the appropriate administrator enablement, user authorization, registration, and consent. | **INFERRED/CONDITIONAL**. No token, cookie, OAuth code, or live API credential was obtained. |
| APSpace and Outlook | Visible read-only surfaces exposed some schedule, attendance/results, mailbox, and calendar metadata. Export, stable IDs, delta behavior, and archival acquisition were not proven. | **UNKNOWN** for unattended acquisition until evidence is gathered. |
| Current Studies Hub | The inspected app has local course, source-mapping, section, resource, file, assignment, page/API, guarded vault, test, and content-hash concepts. Its graph shows the local course view and vault delivery path are connected to explicit tests. | **VERIFIED** prototype capability; not a replacement for the long-term Core. |
| Frappe Framework | The locally inspected Framework snapshot is MIT-licensed and provides a metadata-driven web application stack, database adapters, Redis-backed jobs/cache, scheduler, realtime process, and file model. | **VERIFIED** source and runtime architecture. Its operational footprint is a material product trade-off. |
| Frappe Learning | The locally inspected Learning snapshot is AGPL-3.0-or-later and models courses, chapters, lessons, assignments/submissions, enrollments, progress, live classes, files, certificates, search, hooks, and scheduled jobs. | **VERIFIED** native-LMS capability. No university connector exists in that source. |
| Existing connector code | Source inspection found no APSpace, Moodle, Teams/Graph, Outlook, IMAP, CalDAV, OAuth, delta, webhook, or automatic university connector implementation. | **VERIFIED** absence in the inspected prototype; future discovery must not treat a browser session as a connector. |

The private experimental reports, personal Academic World, real source
observations, credentials, and backups are not source material for this public
repository. This plan records only architecture-relevant, sanitized findings.

### 1.2 Review and amendment discipline

The owner may freeze, amend, or reject any proposed design after review.
Before a material amendment, the editor must identify the affected invariants,
canonical schema, migration/recovery impact, privacy implications, tests, and
unresolved risks. A prototype result or a database implementation never
silently overrides this master plan.

### 1.3 Architectural adaptation

This plan deliberately adapts the architectural discipline studied in the
Accounting & Money master plan: one governing document, explicit decision
status, user-owned canonical records, deterministic authority, preserved
evidence, rebuildable derived state, a filesystem contract, recovery before
convenience, and a model-agnostic typed gateway. It does **not** import
finance-specific entities or workflows. Studies substitutes academic
institutions, offerings, attempts, sessions, sources, originals, mail, and
lifelong learning relationships, with stricter source-account and
university-safety boundaries.

## 2. Executive vision

The intended user-facing shape is:

~~~
Studies/
├── Codebase/
├── Academic World/
└── Launch Studies
~~~

Codebase is software. Academic World is the durable, user-owned academic
archive and living academic record. Launch Studies is one understandable entry
point that starts, opens, diagnoses, updates, and safely shuts down the local
product without requiring the user to understand containers, databases,
Redis, Bench, ports, process managers, or source-control internals.

The product must work completely without Hermes. Removing Hermes must not
remove or impair courses, resources, original files, university archives,
attendance, grades, calendars, deadlines, mail archives, search, offline
access, source provenance, synchronization capability, or the native
application. Hermes, a one-billion-parameter local model, a cloud model, and
any future AI are replaceable clients of a stable deterministic contract.

### 2.1 Product goals

- Preserve an understandable academic life record across current study,
  completed institutions, independent learning, and decades of retention.
- Make original evidence, personal work, provenance, and uncertainty visible
  without requiring the current university portal, an AI, or a live database.
- Provide a capable native application and headless Core that remain useful
  offline and do not require Docker or operator knowledge in normal use.
- Integrate legitimate university and provider sources later without treating
  access, automation, or a title match as proof of canonical identity.
- Scale from a single course to large mail, recording, and document archives
  while keeping ordinary navigation human-readable and recoverable.

### 2.2 Design principles

- One Academic World, one deterministic write authority, and no hidden second
  source of truth.
- Preserve originals and observations; derive indexes, previews, databases,
  and AI context so they can be safely rebuilt.
- Keep one verified byte stream with many relationship/provenance views rather
  than duplicate files for each portal or course folder.
- Prefer explicit evidence, stable IDs, typed relationships, review queues,
  and uncertainty over heuristic or title-only merging.
- Make each durable record inspectable by a person and each mutation staged,
  journaled, validated, recoverable, and testable.
- Treat privacy, least privilege, public-repository safety, platform variance,
  and future account closure as product constraints, not later cleanup.

The governing flow is:

~~~
                         USER
              ┌────────────┴────────────┐
              │                         │
       Native Studies App         Any AI / Hermes
              │                         │
              │                 Studies Skill / Tool
              │                         │
              └───────────┬─────────────┘
                          ▼
                Deterministic Studies Core
                          │
                    Studies Gateway
                          ▼
                    Academic World
       canonical files + evidence + provenance + history
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
    rebuildable search/index       derived database/cache
~~~

The native application calls the same Studies Core directly. AI clients use
the Studies Gateway contract. The Gateway is a stable typed contract, not a
required cloud service, second database, or separate product. The Core may be
an in-process library, a local service, or both; that process boundary remains
a deferred technical decision and may not create a second source of truth.

The governing principle is:

> AI expresses intent. Deterministic software resolves identity, validates,
> persists, journals, and verifies. Academic World stores durable truth.

## 3. Lifetime direction and non-goals

### 3.1 HARD REQUIREMENTS

1. Academic World, not an opaque database, an AI, a UI, a browser profile, or
   a third-party portal, owns durable academic truth.
2. No irreplaceable academic fact, relationship, provenance record, review
   decision, or original byte stream may exist only in a disposable database,
   search index, cache, vector store, Frappe DocType, or AI conversation.
3. Original academic evidence is preserved by default, hash-identified, and
   never silently overwritten or deleted because a remote source changes.
4. One byte-identical object is stored once and can carry many source
   observations and many academic relationships without uncontrolled copies.
5. Stable product-owned identities and relationships outlive display-name,
   folder, university code, offering, portal, and source-system changes.
6. Source-derived information, personal material, and test data remain
   visibly distinct in the filesystem, Core, UI, Gateway, indexes, and logs.
7. A model never invents canonical IDs, chooses canonical paths, reconciles
   ambiguous identities, directly edits canonical files, or writes a database
   as an authoritative side channel.
8. Every AI read and mutation uses one documented, typed, bounded Studies
   Gateway contract. The native app uses the shared Core and cannot create a
   separate academic store.
9. The application remains useful offline after a successful ingest. A
   refresh failure cannot erase the last verified local copy.
10. University connectors are inbound and read-only by default. No
    coursework submission, message, email, attendance, grade, calendar,
    upload, remote delete, or account change is within connector scope unless
    a later owner-approved plan explicitly says otherwise.
11. Browser cookies, sessions, passwords, OAuth codes, authorization headers,
    and hidden tokens are never used as connector inputs or stored in Academic
    World, reports, source control, fixtures, or AI context.
12. The final user experience has no Docker requirement. Existing Docker/
    Bench/Frappe infrastructure remains preserved as a prototype until a
    replacement passes the applicable migration gates.
13. Windows, macOS, and Linux behavior must preserve canonical meaning across
    moves, updates, backups, restores, names, timestamps, and filesystem
    differences.
14. The public source repository contains code, schemas, public-safe
    documentation, synthetic fixtures, and legally permissible vendor source
    only. Academic World and all private runtime data remain local.
15. Every material write, import, source observation, migration, restore, and
    conflict decision is journaled, recoverable, and verifiable.
16. Uncertainty is first-class. The Core presents a review state rather than
    silently guessing that a title, code, filename, deadline, result, or
    source reference is the same thing as another.

### 3.2 PROPOSED baseline decisions, pending owner review

The following form a coherent initial direction but are not frozen in this
draft:

- A product-owned deterministic Studies Core should be the only canonical
  write authority.
- Academic World should use portable, documented human-readable records plus
  strict machine-readable manifests; a Core-built SQLite database should be
  derived and rebuildable.
- A content-addressed object store should preserve one canonical byte stream
  while course folders expose readable record/reference views rather than
  duplicate binary files.
- The long-term app should be a product-owned native Studies experience over
  the Core, rather than treating Frappe Learning records as canonical
  academic truth.
- Frappe and Frappe Learning should remain prototype/reference candidates
  until a no-Docker, file-first, licensing, offline, and headless feasibility
  gate decides between a narrowly isolated Frappe-based implementation and a
  separate product runtime.
- Initial university ingestion should use a source-observation and review
  pipeline before it can update a canonical course or download an object.
- Standard email preservation should use portable MIME/EML message originals
  with optional retained PST, MBOX, MSG, or provider-export containers as
  evidence, subject to the source and user-authorized acquisition path.

### 3.3 Draft architecture-freeze status

This is an authoritative **draft**, not a frozen implementation architecture.
The owner has already established the durable boundaries in the HARD
REQUIREMENTS above: Academic World authority, local-first/offline access, AI
independence, provenance, preservation, public-repository safety, and a
no-Docker user experience. The following remain deliberately unfrozen until
the owner review: the long-term runtime/framework, vendor import, desktop
shell, database/index implementation, exact credential boundary, sync scope,
and distribution/licensing posture. A later owner-approved freeze must list
each decision, its evidence, compatibility consequences, and migration path;
silence never freezes a choice.

### 3.4 Non-goals of this planning run

This plan does not authorize:

- writing new application architecture or scaffolding;
- vendoring Frappe, Frappe Learning, or any other upstream source;
- modifying upstream Frappe or Learning;
- moving away from the existing Docker prototype;
- reorganizing a real Academic World or real Academic Vault;
- downloading a university corpus, archiving a mailbox, or mass
  synchronization;
- creating OAuth applications, requesting permissions, resetting service
  keys, or collecting browser-session material;
- sending messages, email, calendar changes, coursework, grades, attendance,
  uploads, or other university-side changes;
- placing private Academic World data, backups, reports, screenshots,
  identifiers, records, or secrets in this repository.

## 4. Authority boundaries

### 4.1 Academic World

Academic World is the sole durable archive of academic facts, originals,
relationships, provenance, review decisions, and user-authored material. It
is designed to remain browseable in a normal file manager and understandable
with a text editor when the application is absent.

It does not mean that every file may be freely edited without validation. The
Core owns schema-sensitive writes, identity generation, path generation,
hashing, relationship changes, source reconciliation, journal handling,
migrations, and conflict resolution. Supported human descriptive edits may be
accepted only through a documented parse/validate/reconcile path. An AI never
receives a direct file write path.

### 4.2 Codebase

Codebase contains the Core, native app, Gateway implementation, schemas,
launchers, migration code, connector adapters, tests, public-safe templates,
synthetic fixtures, documentation, and eventually legally permissible vendor
source with notices and provenance. Codebase is replaceable software; it is
not the user's academic archive.

No code checkout, Docker volume, Bench site, Frappe database, package cache,
compiled asset, log, local credential, or index is presumed canonical merely
because it is convenient for the current prototype.

### 4.3 Launch Studies

Launch Studies is a named, platform-appropriate entry point. It should:

1. resolve the selected Academic World safely;
2. prevent accidental opening of a copied or incompatible workspace as if it
   were the same writable instance;
3. acquire one-writer coordination;
4. perform a lightweight health/integrity check;
5. make an approved backup or migration decision before a data-changing
   update;
6. start only required local components;
7. open the native UI; and
8. provide clear shutdown, diagnostic, recovery, and offline states.

It must never hide an unrecoverable migration, silently initialize an empty
Academic World over an existing one, or make the user discover a service port
or container command to recover their work.

### 4.4 Repository and private-data boundary

The GitHub repository mhyahya854/LMS is a public-safe source and architecture
repository. It must contain only:

- application and Core source;
- schemas and public-safe configuration templates;
- public documentation and this master plan;
- synthetic fixtures, generated from non-personal examples;
- tests, CI, launchers, migration code, and public-safe release metadata;
- vendor source only when licensing, notices, provenance, and publication
  obligations have been reviewed.

It must never contain Academic World, source originals, mail archives, notes,
grades, attendance, transcripts, recordings, private tickets, credentials,
cookies, tokens, database dumps, Bench sites, private reports, raw diagnostic
bundles, or backups. A defensive repository ignore policy and pre-commit
leakage scan are mandatory before future application work begins.

## 5. Deterministic Studies Core and the native app

### 5.1 Core responsibilities

The Studies Core is product-owned deterministic software. It should own:

- workspace and device identity;
- institution, program, course, offering, attempt, session, resource,
  assessment, email, and event identity;
- source identity aliasing and reconciliation state;
- content hashing, deduplication, versioning, placement, safe file opening,
  and local object validation;
- canonical record schema validation and relation integrity;
- provenance, review decisions, immutable source observations, tombstones,
  journals, operation receipts, and audit history;
- transactional write staging, locks, atomic replacement where available,
  restart recovery, and conservative repair;
- import, download, source-observation, and source-refresh lifecycle;
- explicit conflict, ambiguity, and user-review representation;
- rebuild of derived indexes, database state, search, previews, and caches;
- backup, restore, relocation, migration, health, and integrity operations.

The Core must remain usable headlessly. The native app is a complete optional
client of the Core, not a peer authority. A user who uses no AI must retain
complete access to the same local courses, records, files, searches, archive,
and recovery tools.

### 5.2 Native Studies App

The eventual native app must present, at minimum:

- dashboard and offline/health/freshness status;
- universities, programs, years, semesters, courses, offerings, and attempts;
- lectures/sessions, resources, files, recordings, transcripts, assignments,
  deadlines, exams, attendance, grades, and timetable/calendar views;
- email archive and cross-course references;
- external courses and Islamic Studies as first-class domains;
- local full-text search and source/provenance inspection;
- source status, blockers, conflicts, and review queue;
- backup, restore, migration, diagnostics, settings, and privacy controls.

Its UI may have views optimized for a course, a term, a calendar, a task list,
or an archive, but those are views of one canonical relationship model. It
must show source-derived facts, personal notes, test data, unknown values, and
inferred relationships distinctly. It must not make a remote portal appear
current when only a stale local observation exists.

### 5.3 Headless operation

The Core must support a documented command/API layer for:

- workspace discovery, validation, health, backup, restore, and rebuild;
- bounded entity lookup and provenance inspection;
- staged import and download proposals;
- review/approve/reject/defer decisions;
- local resource opening by stable resource ID;
- explicit source refresh requests after the user has authorized a connector;
- recovery, conflict listing, and integrity scans.

The precise executable language, process split, UI toolkit, and IPC transport
are deferred. They must be selected by compatibility evidence, not by a
desire to mimic the current prototype.

## 6. Studies Gateway and AI contract

Every AI system interacts through one stable, discoverable contract referred
to here as the Studies Gateway. The native app calls the Core directly; it
does not need to invoke an AI or a conversational interface.

The Gateway must provide:

- capability discovery scoped to enabled features and user permissions;
- small, typed read operations such as query.course, query.resource,
  query.deadline, query.provenance, query.search, and query.health;
- typed proposed operations such as import.stage, source.observe,
  review.resolve, note.propose, and backup.verify;
- bounded results containing status, stable IDs, display labels, provenance,
  freshness, ambiguity, warnings, next action, and verification evidence;
- structured errors with plain language, candidate choices, and a safe
  recovery action;
- explicit read-only versus mutation classification, risk class, preview, and
  confirmation policy.

The model may interpret language, select a supported operation, summarize
retrieval, ask for clarification, and explain a verified result. It must not:

- scan the entire filesystem, indexes, database, or Frappe tables;
- fabricate a stable ID, source mapping, course merge, local path, or hash;
- infer an external fact from a title match without Core-supported evidence;
- directly mutate canonical records, source data, connectors, or a database;
- transmit personal notes or source material to a university;
- override a review requirement, permission requirement, or risk class.

### 6.1 Approximately 1B-model usability

A constrained model should receive only task-relevant context, for example a
compact workspace catalog, an entity card, a course card, a list of candidate
matches, an operation schema, and a verified result. It should never need to
reverse engineer institutional naming, walk hundreds of thousands of files,
or understand implementation tables.

The proposed compact contract includes:

- GLOBAL_INDEX.md — a generated human-readable orientation index;
- catalog.json — a bounded catalog of top-level entities and schema/version;
- per-entity _course.md and _course.json style cards;
- JSONL or compact relation manifests with stable IDs;
- source-observation manifests with explicit confidence and review status;
- a typed Studies Gateway that resolves friendly names deterministically.

These are documented interfaces, not hidden prompt conventions. The Core
returns only the subset necessary to complete the current safe task.

### 6.2 Gateway mutation protocol

Any material write follows:

~~~
DISCOVER → READ → PROPOSE → VALIDATE → PREVIEW → APPROVE
         → STAGE → COMMIT → WRITE CANONICAL → UPDATE DERIVED
         → RE-READ → VERIFY
~~~

An operation has a stable idempotency key. Retrying after a timeout, crash,
restart, or lost acknowledgement must return the original result rather than
create another download, relation, note, or archival record. An operation ID
reused with different normalized input is a conflict, not a retry.

Read-only operations may complete without a pointless confirmation. A
canonical relationship merge, destructive action, broad reclassification,
mailbox acquisition, source authorization, or historical rewrite requires a
clear preview and explicit approval. An uncertainty remains an uncertainty
after approval unless the user specifically resolves it.

## 7. Canonical versus derived state

### 7.1 CANONICAL DATA

The following is canonical when it exists:

| Category | Canonical representation and rule |
|---|---|
| Workspace identity and policies | A documented root manifest, durable schema version, selected timezone policy, source registry, and workspace lineage. |
| Academic entities | Stable records for institution, credential/program, term, course, offering, attempt, session, resource, assessment, email, and event. |
| Original evidence | Original downloaded files, preserved email MIME, provider export containers, recordings, transcripts supplied by a source, original calendar files, and original user-authored files. |
| Content identity | Cryptographic content hash, byte size, media type, preservation state, and an object manifest for every preserved byte stream. |
| Relationships | Explicit stable-ID links among entities, source aliases, attachments, content objects, emails, calendar events, notes, offerings, attempts, and review decisions. |
| Provenance | Source system, source object identity, collection method, observation time, source scope, collector/version, safe source reference, original filename/title, revision facts, and actor attribution. |
| Source observations | Immutable or append-only observation records, including seen, changed, unavailable, removed-upstream, denied, failed, and not-checked states. |
| Review and uncertainty | Candidate matches, reasons, evidence references, confirmed/rejected/deferred/unknown decisions, reviewer, time, and prior value/history. |
| User material | User-authored notes, annotations, local tags, personal study records, and their distinct origin/provenance. |
| Durability history | Operation receipts, journals, migration receipts, tombstones, backup manifests, restore records, and audit/change history needed to recover semantic truth. |

Canonical facts use portable JSON records with a documented schema and
canonical serialization rules, accompanied by readable Markdown explanations
where a human needs context. User-authored prose belongs in Markdown or
another directly readable original format; it is never flattened into an
opaque database record. The exact schema language and serializer are a
FUTURE INVESTIGATION, but canonical records must preserve unknown safe fields
or stop with a visible compatibility state rather than delete them on
round-trip.

### 7.2 DERIVED DATA

The following is intentionally replaceable:

| Category | Rebuild source and rule |
|---|---|
| SQL database | Rebuilt from canonical manifests, objects, relations, provenance, and journals. A database may accelerate queries but cannot be the only authority for a course, relationship, or history. |
| Search index | Rebuilt from canonical text, approved extraction, and permitted local object contents. |
| Vector index and AI retrieval cache | Rebuilt locally from approved indexed material. It is never the only copy of an academic fact or personal note. |
| Frappe/MariaDB state | Prototype/runtime state only unless a future Core explicitly writes a complete equivalent canonical record. |
| Thumbnails, previews, transcodes | Recreated from a verified original and tool/version metadata where applicable. |
| Extracted text | Derived when reproducible; preserve it as a separate versioned artifact with source hash, extractor/version, review state, and explicit explanation if later human edits make it durable. |
| UI layouts, sort/filter state, dashboards | Derived preference state that cannot alter academic meaning. |
| Materialized course/resource views | Generated descriptors, links, or optional same-filesystem hardlinks. They can be deleted and rebuilt without losing bytes or relations. |
| Connector acceleration state | Rebuildable when possible; any unreconstructible cursor, user decision, or source failure meaning must also be represented in canonical observation/journal data. |
| Logs and diagnostics | Rotated, redacted derived artifacts. Durable audit facts are written separately to canonical journals. |

The hard recovery test is:

> Delete the derived database, search index, preview cache, and AI index. A
> deterministic rebuild from Academic World must restore discoverability and
> relationships without losing original files, provenance, review decisions,
> or academic history.

### 7.3 Edge case: durable state that is not an original file

Some facts are born as state rather than a source file: a user confirmation,
a source item that disappeared, an unresolved source collision, an operation
receipt, or a human explanation of a relationship. Those facts must be
written as canonical, human-inspectable records or journal entries. A
database row alone is insufficient.

## 8. Academic World filesystem contract

### 8.1 Topology

The proposed long-term tree is:

~~~
Studies/
├── Codebase/
│   ├── README.md
│   ├── app/
│   ├── core/
│   ├── gateway/
│   ├── schemas/
│   ├── tests/
│   ├── fixtures/
│   ├── tools/
│   ├── vendor/                    # only after approved provenance review
│   └── docs/
├── Academic World/
│   ├── README.md
│   ├── _workspace.md
│   ├── Universities/
│   │   ├── Asia Pacific University/
│   │   └── Virtual University/
│   ├── Courses/
│   │   ├── Providers/
│   │   └── Self Study/
│   ├── Islamic Studies/
│   ├── Library/
│   │   ├── Objects/
│   │   └── Exports/
│   ├── Email Archive/
│   ├── Personal Notes/
│   └── Settings/
│       ├── Manifests/
│       ├── Journal/
│       ├── Reviews/
│       ├── Import Inbox/
│       ├── Sync State/
│       ├── Index/
│       ├── Logs/
│       ├── Backups/
│       └── Migrations/
└── Launch Studies
~~~

This is a deliberate contract, not a promise to create all folders
immediately. The Core creates an area only when it has a defined purpose and
may use versioned manifest files instead of excessive tiny folders.

### 8.2 Folder authority table

| Area | Purpose | Authority |
|---|---|---|
| Universities | Human-navigable institutional records and academic views. | Canonical entity cards, references, and user-readable record context. |
| Courses | Non-university learning from providers, private courses, books, certifications, and self-study. | Canonical entity cards and links to shared objects. |
| Islamic Studies | First-class lifelong study domain, independent of university assumptions. | Canonical subject/curriculum/material/note records and links to shared objects. |
| Library/Objects | One preserved byte stream per content hash. | Canonical original bytes and object manifests. |
| Library/Exports | Immutable source-export containers such as a permitted PST, MBOX, archive, or university export. | Canonical originals; never a substitute for source observation/provenance records. |
| Email Archive | Canonical email records and human-readable archive views that reference shared Library objects. | Canonical metadata, EML originals, threads, and relationships. |
| Personal Notes | User-created material not claimed to be source-derived. | Canonical user data, with separate index namespace/policy. |
| Settings/Manifests | Workspace, entity, object, relation, and source manifests. | Canonical structured metadata. |
| Settings/Journal | Append-only operation receipts, audit facts, tombstones, and recovery markers. | Canonical durability history. |
| Settings/Reviews | Candidate reconciliation and explicit human decisions. | Canonical review state. |
| Settings/Import Inbox | Quarantine/staging for partial or untrusted inbound material. | Temporary operational state; accepted/rejected decision and original preservation are journaled. |
| Settings/Sync State | Connector policy, known source checkpoints, and canonical source-observation continuity. | Mixed: durable source facts canonical; acceleration cache rebuildable. |
| Settings/Index | SQL/search/vector/preview index roots. | Derived only; safe to regenerate. |
| Settings/Logs | Rotated local logs. | Derived and redacted; no raw private documents or secrets. |
| Settings/Backups | Backup manifests and verified backup references. Actual backup archives default outside the active workspace. | Manifests/verification are canonical; copies are recovery artifacts. |
| Settings/Migrations | Version maps, preflight reports, and completed migration receipts. | Canonical migration evidence; transient work remains elsewhere. |

There is intentionally no permanent catch-all Config, Mappings, Audit,
Schemas, or Recovery directory. Configuration that changes academic meaning is
manifested; mappings are relationships and source observations; durable audit
belongs in Journal; schemas are versioned with Codebase and referenced by
version; recovery outcomes are journalled. This avoids a decorative folder
taxonomy with overlapping authority.

### 8.3 Root manifest and readable cards

Academic World has one root manifest that declares:

- workspace_id and workspace ancestry;
- format/schema versions and Core compatibility;
- selected canonical timezone/display policy;
- source registry and data-origin vocabulary;
- currently supported relation/object schema versions;
- migration floor/ceiling and read-only behavior for an unknown newer format;
- public/private boundary and backup policy references.

Every independently meaningful entity has, where appropriate:

- a stable immutable ID;
- a display name and filesystem-safe path token;
- a structured manifest;
- a readable Markdown card such as _course.md, _offering.md, or _email.md;
- links by stable ID to related entities and content objects;
- provenance, created/modified facts, review state, and change history.

Paths are organizational aids, not identity. A human folder rename must not
erase a relationship. The Core records a stable ID plus a current path hint and
reports stale/broken hints for repair.

### 8.4 Human-readable courses and one byte stream

The filesystem must be understandable without forcing every copy of every
file into every course folder. The proposed solution is:

1. Preserve each original byte stream once under
   Library/Objects/sha256/<prefix>/<full-hash>/.
2. Store an object manifest beside it: byte hash/size, MIME detection,
   original names, collection events, preservation status, and known
   derivatives.
3. Store course, lecture, resource, assignment, email, and event records in
   the human hierarchy. Each records a resource ID and the one or more object
   hashes it uses.
4. Generate readable per-course resource descriptors containing title,
   original filename, source/provenance, type, version, and local-open action.
5. Let the app resolve a descriptor to its canonical object. Optional
   hardlinks or materialized friendly views may be created only as derived
   conveniences and must never be required for correctness.

This means a person browsing a subject sees a clear Resources, Lectures, or
Assignments view and an explanatory descriptor, while the app opens the one
canonical preserved file. It avoids accidental duplication across Moodle,
Teams, source exports, email attachments, and several course views.

If the same filename has different bytes, it creates a distinct object and
version relation. If a lecturer replaces a file, preserve the previous object,
record the replacement observation, and point a new current-version relation
at the later object. If a remote file disappears, record a source tombstone
or unavailable observation; do not remove the local preserved object.

### 8.5 Safe names, paths, and moves

The Core is responsible for display-name normalization and filesystem-safe
tokens. It must defend against:

- Windows reserved names and invalid characters;
- case-sensitive versus case-insensitive collisions;
- Unicode normalization differences;
- excessively deep/long paths;
- path traversal, symlink, junction, and reparse-point escape;
- untrusted archive extraction;
- source filenames that change or contain control characters.

Original filename is metadata, not a required filesystem path. The Core
generates a safe path and preserves the original name in manifests. A
relocation operation must update only derived path hints and documented local
configuration, verify object hashes and records, preserve workspace identity,
and create a pre-move backup/receipt.

## 9. Stable identity and relationship model

### 9.1 Identity layers

The Core owns product IDs. A source identifier is an alias/provenance field,
not the sole identity of a course or person. The model distinguishes:

| Entity | Why it needs a distinct identity |
|---|---|
| Institution | Different sources, programs, policies, and historical archive boundary. |
| Program/credential | Degree, course of study, completed credential, or learning program. |
| Academic year and term | Human archival navigation and source-term reconciliation. |
| Canonical course | The enduring subject/topic identity independent of an offering title. |
| Offering | A particular institution/source/term/section presentation of a course. |
| Enrollment/attempt | A learner's specific taking, retake, result, attendance, and deadline context. |
| Session/lecture | A dated or undated learning event with materials, recordings, attendance, or notes. |
| Resource/content item | A titled logical item that may point to one or more versions/objects. |
| Content object | One immutable byte stream identified by its cryptographic hash. |
| Assessment/deadline/exam | A task/event with its own lifecycle and source observations. |
| Email/calendar event | One message/event that may relate to many courses. |
| Source identity | One source-system object's stable source key within source/account/scope. |
| Source observation | A fact about a source object at a particular time. |
| Review decision | A human decision that must outlive a candidate match or UI session. |
| Operation | A durable idempotency/recovery boundary. |

The exact syntax can use a collision-resistant opaque identifier plus a
human-readable display code. The syntax is a FUTURE INVESTIGATION; immutable
product identity, namespaced source identities, and Core-only generation are
HARD REQUIREMENTS.

### 9.2 Course, offering, attempt, and retake semantics

One subject can have several names, codes, source aliases, sections, or
semesters without becoming several canonical courses. Conversely, similar
titles must not be merged merely because they sound alike.

The model is:

~~~
Canonical Course
  ├── Offering A: institution + term + section + source aliases
  │     ├── Attempt A1: learner's enrollment, attendance, grade, deadlines
  │     └── Sessions/resources/assessments
  └── Offering B: later term, renamed module, or separate source offering
        └── Attempt B1: retake or separate enrollment
~~~

A retake creates a separate attempt. A cross-semester course has one
canonical course and one or more offerings/attempts. A renamed course retains
the same identity only after evidence or explicit review; otherwise it stays a
candidate. Graduation closes an attempt/program lifecycle without erasing its
records, sources, results, or historical context.

### 9.3 Source mappings and reconciliation

One source identity is unique within a source account/scope. A canonical
course may have many source mappings, but a source identity may not silently
map to two canonical courses. Candidate mapping is separate from accepted
mapping.

Automatic reconciliation requires strong deterministic evidence such as two
independent stable keys, an explicit institution relationship, or a
user-confirmed link. Matching title, abbreviation, lecturer name, filename,
or a similar code is never enough alone. The review record must preserve:

- source platform and source identity;
- observed title/code/term/section/intake facts;
- safe source reference and observation time;
- candidate canonical entities and matching evidence;
- confidence/rationale as a review aid, not authority;
- confirm/reject/defer/unknown decision and reviewer;
- prior decision/history when changed.

The synthetic local course and simulated source mappings remain test data.
They must never be promoted into real academic mappings.

### 9.4 Provenance and source state

Every source-derived entity, field, and object has provenance sufficient to
answer:

- What source asserted it?
- Which source identity and source scope was observed?
- When was it observed, in which timezone, and by what method/version?
- Is the value original, normalized, derived, user-confirmed, or uncertain?
- What original object, page/export, message, or observation supports it?
- Is the source currently reachable, stale, removed-upstream, denied, or
  unknown?

Source state is not a destructive command. A remote rename becomes a rename
observation. Remote deletion becomes an explicit tombstone or availability
state, retaining the local evidence. A source that later becomes unavailable
after graduation is ordinary archival reality, not a reason to erase local
history.

## 10. Human academic structures

### 10.1 Asia Pacific University

The primary human view is:

~~~
Universities/
  Asia Pacific University/
    Program/
      Year 1/
        Semester 1/
          <Subject>
        Semester 2/
          <Subject>
      Year 2/
      Year 3/
      ...
~~~

This is a human navigation and archival structure, not a claim that source
portals use the same year/semester vocabulary. Institutional module code,
offering code, intake, campus, degree level, source title, section, portal
ID, and date range remain explicit metadata/provenance. A source term may be
shown in the human hierarchy only after evidence or marked as observed/
provisional.

Each subject view can expose:

- course/offering/attempt card and source mapping status;
- lectures/sessions and associated resources;
- assignments, exams, deadlines, submissions as preserved evidence, and
  result/review status;
- recordings, supplied transcripts, generated transcript derivatives, and
  note links;
- attendance records, results, grades, timetable/calendar events, and
  administrative evidence;
- source observations, original files, local-open actions, and personal notes
  marked separately.

The human view must remain understandable after graduation. It must preserve
renamed modules, retakes, archived offerings, changed term labels, course
withdrawals, assessments, academic notices, program history, final transcript,
certificate/graduation evidence, support/appeal material where deliberately
retained, and source-system disappearance.

### 10.2 Virtual University

Virtual University is a completed historical archive, not a forced copy of
the APU structure. Its root should preserve only evidenced historical
program/semester/subject relations while allowing a coherent archive for:

- credential/program and completion/graduation records;
- semesters and subjects where records exist;
- course materials, assignments, submissions, feedback, results, and
  transcripts;
- final-year project/proposal/development/submissions/supervisor feedback;
- university correspondence, tickets, attachments, support evidence, and
  certificates;
- source provenance and gaps where records were unavailable.

A completed institution has a different lifecycle: discovery/import is
archival, sources may already be closed, and the UI emphasizes long-term
retrieval, provenance, and preservation rather than current deadlines.

### 10.3 External Courses

Academic World/Courses supports non-university learning without pretending it
is a university. Provider, course, module, instructor, certificate, learning
plan, book, curriculum, resource, progress, and personal note records may be
present as applicable. Examples include professional platforms, vendor
training, certification providers, open courseware, books, and self-study.

An external course can use the same canonical Course, Offering, Attempt,
Resource, Assessment, and provenance primitives. University-only concepts
such as official attendance, transcript, or grade are optional and never
forced into its schema.

### 10.4 Islamic Studies

Islamic Studies is a first-class domain with its own human-friendly
organization, not a fake university:

~~~
Islamic Studies/
  Curricula/
  Subjects/
  Books/
  Teachers/
  Courses/
  Readings/
  Qur'an/
  Memorization/
  Notes/
  Sources/
~~~

The logical model supports Qur'an study, tafsir, hadith, fiqh, aqidah, seerah,
Arabic, Islamic history, books, teachers, curricula, lessons, readings,
memorization, revision, source citations, and progress. It does not populate
religious content or impose a single school/curriculum in this plan. It shares
the Core's identity, evidence, provenance, offline, search, and note
boundaries while retaining its own domain vocabulary.

### 10.5 Notes, recordings, transcripts, attendance, grades, and time

Personal notes have a Personal origin and an explicit sharing/index policy.
They may link to a course or resource but do not become source-derived merely
because they sit beside it. Test data is similarly marked and excluded from
ordinary records and source reconciliation.

Recordings are large original objects with recording-specific metadata:
source, duration when known, capture/availability date, versions, consent/
rights constraints, related session, and optional generated derivatives.
Supplied transcripts are originals; generated transcripts retain source
recording hash, tool/model/version, language, segmentation, confidence/review
state, and never overwrite a supplied original.

Attendance, grades, results, transcripts, exam schedules, and calendar events
are observations with source, time, scope, and revision state. They can be
displayed as current local facts only when their provenance/freshness is
visible. Corrections remain historical revisions. A withheld/incomplete/
disputed grade remains such; the Core does not manufacture a value.

Time records distinguish source date-only values, local instant, source
timezone, display timezone, recurrence, updated time, due time, exam time,
event cancellation, and uncertainty. The current institution's published
timezone cannot be silently rewritten into the user's present timezone or
vice versa. DST, clock skew, changed rooms, cancellations, recurring events,
and source timezone ambiguity require explicit representation.

## 11. University email archival

### 11.1 Purpose and authority

University mail is potentially irreplaceable after graduation or account
closure. The final product must support a lawful, user-authorized archive of
the user's own university mailbox without treating selected current messages
as the whole archive. The archive must retain enough original evidence to
remain useful decades later without the university account, Outlook, Hermes,
or the Studies app.

One canonical message is stored once and can be referenced from many courses,
projects, deadlines, administrative issues, and source observations. A message
or attachment must not be physically copied into each course folder.

### 11.2 Canonical format policy

The proposed hierarchy is:

~~~
Academic World/
  Email Archive/
    Accounts/
      <account-display-token>/
        _account.md
        Folders/
        Messages/
        Threads/
        Exports/
~~~

The preferred per-message original is MIME/EML where a supported source path
can retrieve it faithfully. EML preserves RFC-style headers, MIME body parts,
inline content, attachments, and calendar messages in a broadly portable
format. The canonical message record must point to the byte-preserved EML
object and contain the message's stable product ID, Internet Message-ID when
present, provider identifier(s), thread/conversation facts, account/folder
observations, sender/recipient metadata, time facts, subject, attachment
relationships, source provenance, and review state.

PST, MBOX, MSG, and equivalent provider archives have distinct roles:

| Format | Planned role |
|---|---|
| EML | Preferred portable per-message original when acquired faithfully. |
| PST | Preserve as an immutable source-export container and coverage evidence when Outlook export is the authorized acquisition method. Do not rely on it as the sole normal per-message contract. |
| MBOX | Preserve as an immutable batch source where a lawful exporter supplies it; parse into canonical message records only through a journaled import. |
| MSG | Preserve if it is the original source artifact, especially for compatibility, but do not require it as the cross-platform primary archive. |
| ICS/iCalendar | Preserve calendar-invitation/event originals as related objects; do not flatten recurrence or organizer facts into a summary only. |

If a provider/export cannot furnish EML, preserve its original container and
record the import limitation rather than fabricating richer fidelity. A
portable conversion is a derived artifact unless it has been carefully
validated against the original and labelled accordingly.

Microsoft documents that a mailbox export can produce a PST on supported
desktop Outlook paths, and that Graph can return message MIME content through
a dedicated message-content endpoint. Those are future, user-authorized
acquisition candidates, not permission to export or register anything now.

### 11.3 Message, attachment, and calendar relationships

The archive must preserve:

- original MIME headers and bodies, both HTML and text parts where present;
- sender, recipient, reply-to, date, received date, Message-ID,
  In-Reply-To/References, conversation/thread identifiers when present;
- provider/account/folder/category/label observations and read/unread state
  only when it is useful and lawfully available;
- attachments as shared content objects with original part name, MIME type,
  Content-ID, disposition, hash, and message-part relation;
- inline images and rich-body references without losing the body/original;
- meeting invitations, cancellations, and calendar attachments as their own
  source objects;
- source/delegated acquisition method, time, consistency/coverage scope,
  exporter/adapter version, and any gaps;
- course/project/issue references as explicit relationship records.

Deduplication must prefer stable message identity where present, then
conservative hash/header identity. The same attachment shared by many emails
is one object with many message-part references. A same-looking email with
different MIME bytes is not silently collapsed. A corrected, moved, or later
re-synchronized message is a later observation/version, not an overwrite of
historical evidence.

### 11.4 Acquisition, privacy, and account closure

Before any archival acquisition, the user selects the account, scope, folders,
history range, acquisition method, and expected privacy impact. The importer
creates a manifest, starts an idempotent journalled operation, preserves
original data, identifies coverage gaps, and validates the local archive
without changing the remote mailbox.

The product must never use browser sessions, scrape a browser, capture
cookies/tokens, mark messages read, alter folder state, send mail, or infer
that a visible mailbox means an archive is complete. Connector permissions,
retention, legal/contractual limits, messages from other people, data
minimization, local encryption preferences, and redacted diagnostic output
need explicit review. All mail content and attachments remain outside Git.

## 12. Source observations, connectors, and synchronization

### 12.1 Inbound, read-only safety model

The first supported mode is always source discovery and observation. It is
read-only and cannot mutate university systems. An adapter is not allowed to
send messages, submit coursework, upload files, alter attendance/grades,
change events, create teams, or delete/rename remote objects.

No connector implementation begins until it has:

1. an explicit product requirement and source-specific authorization;
2. a documented source identity and scope model;
3. a least-privilege supported authorization method;
4. a source-observation, provenance, reconciliation, and tombstone design;
5. idempotency, retry/backoff, pagination, rate-limit, and pause/resume
   behavior;
6. a synthetic test fixture and an isolated local test root;
7. an offline, privacy, recovery, and source-write boundary review.

### 12.2 Source observation lifecycle

The normal source lifecycle is:

~~~
DISCOVER SOURCE
  → AUTHORIZATION GATE
  → LIST/OBSERVE METADATA
  → PRESERVE RAW-SCOPE FACTS AS ALLOWED
  → STAGE CANDIDATES
  → RECONCILE/REVIEW
  → OPTIONAL INBOUND DOWNLOAD
  → HASH/QUARANTINE/VALIDATE
  → COMMIT CANONICAL OBJECT/RELATION
  → UPDATE DERIVED INDEX
  → VERIFY OFFLINE OPEN
  → RECORD FRESHNESS/CURSOR/RESULT
~~~

Each observation records source system, source-account scope, source object
identifier, parent/container identity where known, collection time, displayed
time/timezone, safe source reference, normalized fields, raw-preservation
policy, adapter version, result/status, and relation candidates. The Core
must distinguish:

- observed and verified locally;
- observed but not downloaded;
- candidate mapping needs review;
- download queued, partial, validated, or rejected;
- source access denied, expired, paused, rate-limited, failed, or unknown;
- source object changed, renamed, unavailable, or removed-upstream.

An observation does not become a local canonical course field merely because a
source returned it. Reconciliation and review determine whether/how it relates
to an existing academic entity.

### 12.3 Download/import lifecycle

The Core processes inbound objects through:

1. create a durable operation ID and source/download manifest;
2. fetch only through an authorized, supported, bounded adapter;
3. stream to a private staged file while measuring size and hash;
4. enforce allowed source, expected media, size, archive-bomb, malware, and
   path policies;
5. preserve a partial-download receipt on interruption without treating it as
   an original;
6. validate the completed byte stream and identify a duplicate/concurrent
   object by hash;
7. promote a validated object atomically to Library/Objects;
8. write source observation, object relation, resource/version relation, and
   journal receipt;
9. update only derived indexes/previews; and
10. re-read the object and verify its local-open behavior before reporting
    success.

Remote replacement produces a new object/version relation. A remote deletion
or unavailable source never triggers local deletion. A failed refresh leaves
the last verified local object and its previous provenance intact.

### 12.4 Incremental refresh and operational discipline

When a source later supports incremental retrieval, the connector must:

- retain a source-specific opaque cursor/revision/ETag only inside the
  approved connector state boundary;
- make pagination resumable with durable checkpoints;
- assign idempotency keys to page, object, and commit operations;
- use source-specific rate limits, bounded retries, exponential backoff, and
  clear pause/resume states;
- record a stale/partial/failed run instead of presenting an old result as
  current;
- preserve observed remote deletion/rename facts as tombstones/observations;
- make historical snapshots and replays explicit, versioned, and reviewable;
- avoid whole-corpus re-downloads when a safe delta/modified-time path exists;
- avoid treating a source's modified timestamp as the sole identity or
  conflict key.

Cursor data that can be reconstructed is derived. A source-observation
continuity fact, manual checkpoint decision, or irrecoverable state must also
be journalled canonically. A connector does not silently resume after a
credential, policy, schema, or scope change.

### 12.5 Authentication and secrets

Connector secrets belong in the operating-system secret store or an
implementation-selected local credential boundary, referenced by a
non-secret identifier. They do not belong in Academic World files, Codebase,
Git, logs, backups, email records, fixtures, or AI context.

The Core must use provider-supported authentication only. It must request
specific user action for a password, 2FA, OAuth consent, administrator
approval, service token, or export choice. A missing authorization blocks that
adapter but does not block other local/offline work. The user can revoke,
replace, or disable an authorized connector. The UI reports access scope,
last success, last failure, and data retained locally without exposing a
secret.

### 12.6 Current service-specific position

| Service | Verified present evidence | Plan position |
|---|---|---|
| Moodle | Read-only dashboard metadata was observed; deeper course acquisition is blocked by an authentication boundary. Official service/mobile paths are conditional on site enablement and user-specific authorization. | No connector now. Future read-only adapter begins only after a supported authorization and source-capability proof. |
| APSpace | Read-only UI shows relevant academic surfaces; no supported export/API/delta/offline acquisition was proven. | Treat as manual/source-observation first. Do not infer API or automation capability from UI visibility. |
| Microsoft Teams | Read-only team/channel metadata and one manual inbound SharePoint-backed file download were verified. | A manual download is not a Graph connector. Future adapter requires supported delegated authorization, least privilege, and file/permission/delta evidence. |
| Outlook/Microsoft 365 | Mailbox and calendar metadata was observed read-only; message/archive/export/delta behavior was not proven. | Design complete email preservation first. Future acquisition requires supported consent/export and strict no-write behavior. |
| Frappe Learning | Native course/lesson/assignment behavior exists locally. | It is not a university source connector or a substitute for source observation/reconciliation. |

The current local source candidates remain unmerged. Different source codes,
titles, terms, or sections may describe different offerings even if their
names resemble each other.

### 12.7 Offline-first behavior

Once an object or source observation is successfully committed:

- local open/search works with all university services unreachable;
- source freshness and known staleness remain visible;
- a missing Core database triggers rebuild rather than loss;
- a source failure cannot hide the last verified object;
- local personal notes never leave the device through a source refresh;
- a user can inspect the original, object hash, source observations, and
  review decisions without an AI or a network.

The existing synthetic vertical slice is a regression baseline for this
principle. It does not establish a claim that real source synchronization
already works.

## 13. Frappe and Frappe Learning architecture evaluation

### 13.1 Evidence from inspected source

The current Frappe Framework is a full-stack web application framework. Its
document/ORM model, database adapters, files, cache, scheduled work,
Redis-backed queue workers, realtime components, Bench process topology, and
database service are materially useful prototype capabilities. Frappe's own
documentation identifies database, Redis queues/cache, workers, scheduler,
web, and realtime processes as components of a running environment.

For reproducible planning evidence only, the inspected prototype snapshots
reported Framework commit `012667b9c4e7f66d5e1ff5858d2e922331d4300a`
(release `16.35.0`, MIT) and Learning commit
`2ee61568603d0b081e9d98c8bf39b18f4464e3b5` (release `2.63.0`,
AGPL-3.0-or-later). These observations are not a vendor pin, an import, or a
commitment to either runtime.

The inspected Frappe Learning source is a native LMS, not an academic archive
or university aggregator. It supplies courses, chapters, lessons, progress,
enrollment, quizzes, assignments/submissions, live classes, files,
certificates, search, permissions, scheduled jobs, and a browser-oriented
frontend. Its source includes an AGPL-3.0-or-later license; Frappe Framework
is MIT. Any future vendor or distribution decision must obtain competent
license/compliance review rather than assume that a private desktop intent
removes obligations.

The existing Studies Hub demonstrates useful concepts:

- explicit canonical course/source mapping records;
- separation of source-derived, personal, and test material;
- guarded local file access and content hashing;
- browser-visible provenance and local/offline proof;
- tests for mapping uniqueness, source/personal separation, path safety,
  duplicate bytes, and same-name different bytes.

It does not solve the long-term Core requirements: file-authoritative
canonical state, durable journal, cross-platform no-Docker packaging, full
email archive, source lifecycle, connectors, immutable identities, migration,
and database rebuild from Academic World.

### 13.2 Option comparison

| Option | Benefits | Material conflicts/risks | Draft assessment |
|---|---|---|---|
| A. Upstream Frappe Learning plus Studies Hub extensions | Preserves existing prototype usability, mature course/lesson UX, lowest divergence. | Frappe database/Bench lifecycle remains central; Learning's model is not file-authoritative; university aggregation/email/archive needs sit outside it. | Viable prototype continuity, weak as the whole lifetime architecture. |
| B. Vendor a fixed Frappe Learning snapshot plus Studies-owned modifications, while retaining upstream Frappe | Fixed Learning source provenance and full local control of Learning changes without vendoring the Framework itself. | Patch ledger, security/update burden, AGPL compliance, and continued dependency on a compatible Frappe/Bench/Redis/database runtime. | Viable only if measured Learning reuse justifies the compliance and runtime cost; not selected. |
| C. Vendor Frappe Framework plus modified Learning and Studies Core | Full control over both source layers and an exact reproducible foundation. | Highest divergence, upgrade/security/testing load; AGPL implications; still inherits a web/database/worker architecture that may conflict with simple file-first no-Docker UX. | Not justified by present evidence; may be revisited only with an explicit vendor feasibility gate. |
| D. Use Frappe as infrastructure but build a product-owned Studies UI/Core | Lets existing framework skills support a custom product domain. | Still needs a decision about Frappe's services and database authority; may duplicate Learning UI and remains coupled to Frappe runtime constraints. | Stronger than A/B for domain boundaries, but must prove no-Docker and Core separation. |
| E. Replace Frappe for the final product after harvesting permissible concepts | Cleanest route to file-first Core, portable data, native app, and minimal local service topology. | Requires more product UI/core work and careful reuse/license review; maturity must be built or selected. | Plausible long-term target, but not selected without a comparative feasibility proof. |

### 13.3 Draft conclusion and decision gate

**DEFERRED DECISION — final framework/runtime choice.**

The evidence does not support freezing any option today. It does support
freezing the product boundary: Academic World and Studies Core must remain
independent of Frappe/Learning internal tables, and no Frappe database may
become the only academic archive.

The first implementation feasibility gate must compare D and E against the
hard requirements and retain A/B only as prototype/migration compatibility
options. It must prove, using synthetic data:

- headless Core operation with no Frappe database as authority;
- rebuild of all derived state from a small Academic World fixture;
- offline launch and local file opening;
- no-Docker user experience on target operating systems;
- one-writer/recovery behavior;
- native UI access to the same Core;
- source/provenance/review model fit;
- licence/compliance/distribution implications;
- maintenance, security update, and migration cost.

Frappe Learning may still be a valuable fixed-source foundation if this gate
demonstrates genuine reuse value and the owner accepts its license and runtime
consequences. A fixed snapshot must not be imported merely because the
prototype already uses it.

### 13.4 Vendor provenance policy

No GitHub fork is required. A future approved vendor import must record before
copying source:

- upstream repository and official source URL;
- upstream release/tag and exact commit;
- source-tree cryptographic digest and import date;
- license text, notices, copyright/attribution, and transitive obligations;
- clean-source verification and source acquisition method;
- intended modification boundary, patch/decision ledger, and update policy;
- SBOM/release provenance requirements;
- legal/compliance approval and publication/distribution implications.

The owner must decide whether a fixed snapshot is a maintained foundation or
whether upstream security/compatibility merges are required. Neither a fork
nor an upstream merge program is assumed. A future import must never conceal
local modifications as upstream code, and it must never pull Academic World
content into source control.

### 13.5 Graphify and extension architecture

Graphify can remain an optional derived code/document knowledge graph. It may
help developers understand Core, adapters, schemas, and migrations, but its
graph, embeddings, extracted summaries, and reports are derived and must not
be canonical academic authority.

Future plugins/adapters must have a narrow product-owned interface:

- declare input/output schemas, capability, scope, and supported source;
- run under a Core-owned permission, journal, retry, and data-origin policy;
- return source observations/candidate objects, not direct canonical writes;
- expose no generic filesystem, credential, or remote-write escape hatch;
- be disabled/replaced without loss of Academic World data.

## 14. No-Docker runtime and cross-platform direction

### 14.1 HARD REQUIREMENT: no-Docker user experience

The final product must not require Docker. The current Docker stack remains a
valuable prototype and preservation target until a replacement is proven. The
user must be able to select/open Academic World and invoke Launch Studies
without learning containers, MariaDB, Redis, Bench, ports, supervisor,
systemd, or terminal commands.

Frappe can be operated outside Docker, but its documented Bench topology
still involves database, Redis, workers, scheduler, web, and realtime
processes. That is evidence against casually calling a native Bench install a
completed no-Docker product experience. A Frappe-based option must hide,
install, supervise, update, and recover those components safely or fail the
runtime gate.

### 14.2 Proposed runtime shape

The preferred direction is a locally packaged launcher plus Core that:

- treats Academic World as an explicit user-selected data root;
- stores derived SQLite/search/cache state beneath Settings/Index or an
  equivalent derived local cache;
- starts a minimal local process set only when necessary;
- uses authenticated local IPC rather than exposing an unauthenticated
  network service;
- uses one-writer coordination and consistent read snapshots;
- opens the native app after a health check;
- gives a plain-language recovery screen if migration, lock, backup, or
  derived-state rebuild fails;
- stops child processes cleanly on exit and recovers after crash/restart.

The UI shell, Core language, installer format, local IPC choice, and update
technology are DEFERRED DECISIONS. They must be chosen through prototypes on
Windows, macOS, and Linux, not assumed from the current Docker stack.

### 14.3 Platform-specific gates

| Platform | Required proof |
|---|---|
| Windows | Installer/portable launcher, one-writer behavior, long/Unicode paths, reparse-point safety, local secret storage, safe open, update/rollback, and no dependency on WSL/Docker for normal use. WSL may be a transitional implementation detail only if Launch Studies fully owns the experience. |
| macOS | Signed/notarized distribution plan where applicable, app/helper lifecycle, sandbox/permission behavior, Unicode normalization, file locking, external-drive behavior, update/rollback, and safe open. |
| Linux | At least a documented portable package/install strategy, user-level process lifecycle, filesystem/lock behavior, desktop integration, update/rollback, and external-drive behavior. |

The canonical records and Gateway semantics must be identical across
platforms. Differences in UI shell, package manager, process supervisor, or
file dialog must not alter a stable ID, content hash, provenance, relation,
timezone fact, or review result.

### 14.4 OneDrive, cloud folders, removable media, and concurrency

Academic World may be placed in a user-controlled cloud-synced or removable
location only after the Core explains the trade-offs. Cloud sync is not a
distributed transaction coordinator. The Core must detect provider conflicts,
partial download placeholders, timestamp churn, and duplicate events; it must
not use timestamp-only last-writer-wins to resolve source/canonical changes.

The initial policy is one coordinated writer per workspace with concurrent
consistent reads. A stale lock holder must be fenced before it can write
again. Simultaneous writes from two devices are unsupported until a tested
merge/coordinator design exists. An external drive removal, partial copy,
network share, or unclean shutdown triggers read-only/recovery mode rather
than silent repair.

## 15. Safe writes, conflicts, backups, recovery, and migrations

### 15.1 Canonical write protocol

Any Core operation that changes one or more canonical records must be
transactional at the product level even when the filesystem cannot offer a
database transaction. The proposed protocol is:

1. Acquire the workspace writer lease and verify fencing/revision state.
2. Read and hash all affected canonical inputs and related manifests.
3. Resolve stable identities and validate schemas, ownership, relations,
   provenance, source policy, and requested transition.
4. Create a complete staged change set in a private sibling staging area on
   the same filesystem where practical.
5. Write an intent journal entry with operation ID, workspace ID, actor,
   base hashes/revisions, intended files, expected hashes, and recovery plan.
6. Flush staged originals/manifests and validate their schemas/hashes.
7. Atomically replace or rename individual files where platform guarantees
   permit; otherwise record the weaker guarantee and preserve a recoverable
   two-phase marker.
8. Write a durable commit marker.
9. Refresh derived state incrementally or mark it stale/rebuildable.
10. Re-read canonical records and objects, verify expected hashes/relations,
    then mark the operation completed and release the writer.

The result is either a valid pre-operation state, a valid complete
post-operation state, or an explicit recovery state. It must never silently
report success after a partial multi-record relation, half-promoted file,
ambiguous merge, or incomplete migration.

### 15.2 Conflicts and manual edits

The Core detects conflicts using stable IDs and content/revision baselines,
not timestamps alone. A conflict can arise from a human file edit, UI write,
Gateway operation, cloud-sync conflict copy, old app version, source refresh,
or recovery replay.

The initial behavior is conservative:

- a supported descriptive human edit is parsed, validated, journalled, and
  reconciled through the Core;
- a semantic change to source provenance, identity, relation, source state,
  review decision, or object link requires a typed Core operation;
- stale or overlapping changes preserve the base/local/external versions and
  enter review;
- an automatic merge is permitted only for explicitly declared
  non-overlapping fields with deterministic semantics;
- timestamp-only last-writer-wins is prohibited;
- a malformed record, duplicate ID, dangling object, or invalid schema
  triggers a visible repair/review state rather than silent normalization.

The user-facing review must state which record, fields, IDs, objects, source
observations, base version, and choices are involved. It must offer a safe
defer/export/restore path where a complete automatic resolution is unsafe.

### 15.3 Backups and restore

Before a data-changing migration, bulk operation, significant source import,
or restore, the Core creates and verifies a snapshot. Backups normally live
outside the live Academic World to avoid recursive copies and reduce damage
from one filesystem failure.

A verified snapshot includes or references:

- workspace identity/lineage, format version, capture boundary, and tool
  version;
- canonical manifests, journals, review records, original objects, exports,
  notes, and source-observation history;
- file/object inventory, byte sizes, hashes, and relation validation result;
- backup creation/verification status and any known exclusions;
- enough derived-state information to rebuild indexes if desired, without
  treating derived state as the only recovery path.

Restore has separate modes: inspect/verify, compare, recover selected
canonical records, replace a workspace, or create an explicitly new fork.
It never silently merges two roots with the same workspace ID, overwrites
current records, or treats a missing backup file as proof that a source never
existed. A restore is staged, journalled, schema/relationship/hash checked,
and verified before being made writable.

### 15.4 Migration and update safety

Normal software updates must not imply permission to rewrite, delete, or
reinterpret academic history. A canonical schema migration follows:

1. detect version compatibility before opening for mutation;
2. explain the scope and whether migration is genuinely required;
3. preflight free space, locks, schema support, and source compatibility;
4. create/verify a recoverable snapshot;
5. stage and dry-run where technically reasonable;
6. journal the migration, apply deterministic transformations, and preserve
   unknown extension fields;
7. validate IDs, original object hashes, relations, provenance, review
   decisions, current semantics, and derived-state rebuildability;
8. compare the migrated workspace to the protected snapshot for preservation
   of academic meaning; and
9. stop in recovery/read-only mode on any anomaly.

An old app reading a newer workspace must report a compatible read-only state
or refuse clearly. It must never downgrade data, discard unrecognized fields,
or write a partial older representation. Derived-index schema upgrades can be
rebuilt separately from canonical migrations.

### 15.5 Integrity, corruption detection, and salvage

The planned Studies doctor/Health capability performs read-only checks for:

- duplicate/missing IDs and malformed manifests;
- broken or type-invalid relations;
- missing, corrupt, changed, or orphaned content objects;
- object hash/size/media mismatch;
- unfinished journal or migration operations;
- stale/failing derived index;
- unresolved source review/candidate collision;
- invalid source status transition or unsafe local path;
- backup inventory/hash/snapshot mismatch;
- unsupported schema/version;
- incomplete download, recording, transcript, or email import;
- unsafe reparse point, symlink, archive, or path token.

Repair must be explicit, previewable, journalled, and reversible where
possible. Preferred repair is rebuild derived data, restore a verified
original, quarantine untrusted/partial input, or surface a review item.
Repair must not fabricate a grade, course relation, source observation,
calendar event, or original byte stream merely to make a health check pass.

### 15.6 Crash recovery and fault injection

Tests must terminate Core work at every important boundary: before/after
staging, after journal intent, between multi-file replacements, before/after
commit marker, after canonical commit but before index update, during backup,
during restore, during file promotion, and before acknowledgement.

After restart, the Core inspects every incomplete operation and determines
pre-commit, fully committed, or explicit partial/recovery state from
durable evidence. Representative tests include:

- a single content object referenced from two sources;
- a course/offering relation update plus a personal note reference;
- a source object replacement with prior version preservation;
- an email plus shared attachment object import;
- a migration interrupted between manifests;
- backup/restore interrupted after staging;
- a lock holder crash and a safe subsequent writer.

## 16. Derived database, search, media, and scale

### 16.1 Index/database strategy

The default derived store should be a local SQLite database or an equivalent
embedded, portable, rebuildable store selected in the Core feasibility phase.
It may hold denormalized entity lookups, full-text metadata, relation maps,
search ranking, freshness views, content hashes, derived aggregates, and
pagination support. It must never be the only location of an entity,
relation, source observation, review decision, or original object.

The Core incrementally updates only affected derived entries after a verified
canonical commit. Startup performs a cheap manifest/journal/index-version
check and rebuilds fully only when the index is missing, corrupt, outdated, or
integrity checks require it. File watching is an optimization, not the sole
truth source; an explicit rescan is always available.

### 16.2 Search and text extraction

Search is local-first. It indexes only permitted local content and labels
results with data origin, source, freshness, type, and confidence. It should
support structured filters across institution, program, year, semester,
course, offering, source, resource type, date/time, review state, and
personal/source/test origin.

Text extraction is isolated from originals:

1. preserve/verify original object;
2. run an isolated parser/extractor under file-size/time/sandbox policy;
3. store extracted text as a derived version with source object hash,
   tool/version, language, error/warning, and review state;
4. index it only under allowed privacy policy;
5. invalidate/re-extract when its original hash changes, without deleting
   the old original or claiming the extract was authored by the source.

Prompt injection or instructions inside a PDF, slide deck, email, transcript,
or file are untrusted content. They cannot alter Gateway policy, Core
authority, source scope, or write decisions.

### 16.3 Large media and previews

Large recordings, scans, slides, PDFs, mail archives, and provider exports
are opened lazily. The app should stream/range-read a local canonical object
when the platform supports it, show verified metadata before expensive work,
and make preview/transcode generation cancellable and derived.

Thumbnails, waveform/proxy media, PDF renderings, OCR, transcript alignment,
and preview HTML are derived. A failure to create them leaves the original
available and must not block ordinary backup/restore. Multiple recordings per
lecture, recordings without transcripts, transcripts without recordings, and
several independently sourced files for one session remain explicit
relationships—not forced one-to-one fields.

### 16.4 Performance and archive scale

The product must be measured against synthetic, public-safe workspaces
representing at least:

- tens of thousands of objects/records;
- hundreds of thousands of objects/records;
- long-running email and media archives;
- many institutions/programs, retakes, source aliases, and decades of
  history;
- large but sparse resource folders and very large single source exports.

Measure first launch, incremental scan, full rebuild, course navigation,
search, email retrieval, local object open, preview generation, backup,
restore, migration, conflict view, and focused Gateway lookup. The Core
loads the relevant course/date/result window rather than every record or file
into memory. Any sharding or alternate index must preserve documented
identities, source relations, and human-readable navigation.

## 17. Security, privacy, and repository safety

### 17.1 Local privacy

Academic World may contain highly personal academic records, correspondence,
identifiers, grades, attendance, recordings, and notes. The product defaults
to local processing, data minimization, and explicit disclosure. It should
support local filesystem permissions, safe secret references, optional
encryption investigation, redacted diagnostics, secure temporary-file policy,
malicious file/archive defenses, and safe-open behavior.

Encryption at rest, if implemented, must preserve one logical Academic World
and documented recovery/backup/restore semantics. AI clients never receive raw
keys or passwords. The decision on default encryption, key storage, recovery,
rotation, and loss handling is a DEFERRED DECISION requiring a dedicated
threat/recovery review.

### 17.2 GitHub boundary and defensive ignores

The repository must include a defensive .gitignore from its first commit.
It must reject Academic World, local runtime/state, local environment files,
database dumps, backups, logs, credentials, tokens, recordings, raw
exports, and accidental source downloads. Future CI and local pre-commit
checks must scan staged content for secrets, known private-root patterns,
emails, large binaries, and unapproved fixtures without uploading the
workspace to a third party.

Public examples use generic institutions, courses, people, identifiers,
dates, grades, and email bodies. A real artifact may influence a decision
only through sanitized architecture findings; it is never copied into plan
history or a test fixture.

### 17.3 Release, supply chain, and licensing

Before a public product release, define:

- dependency lock/provenance, vulnerability review, SBOM, reproducible build
  goal, signing/notarization, and secure update verification;
- vendor source notices, licensing, source availability obligations, and
  modification ledger;
- no-private-data build/test/diagnostic checks;
- supported-platform compatibility and rollback behavior;
- incident/repair process that does not request unneeded academic data.

AGPL-related distribution/network obligations for any Frappe Learning or
derived work require a competent legal/compliance review before a vendor
decision. This is a decision gate, not a legal conclusion.

## 18. Testing, CI, fixtures, and validation

### 18.1 Test philosophy

A test is incomplete if UI output looks correct but canonical files,
provenance, recovery, privacy, or offline behavior are wrong. Every future
feature must prove both its deterministic Core outcome and its filesystem
outcome using synthetic public-safe fixtures.

The retained synthetic Studies Hub vertical slice is useful regression
evidence: it already demonstrates a local course, three synthetic mappings,
resources, local-file opening, deadline, provenance/personal distinction, and
an offline claim. It must be preserved as a prototype artifact but cannot
substitute for Core conformance tests.

### 18.2 Required test layers

- unit tests for IDs, schema validation, paths, hash/object rules, relation
  integrity, source-state transitions, dates/timezones, and media policy;
- golden-workspace tests for all canonical entity kinds and readable cards;
- property/fuzz tests for duplicate IDs, malformed manifests, invalid paths,
  Unicode/case collisions, partial writes, archive bombs, and parser input;
- Core mutation/recovery tests for staging, journal, idempotency, conflict,
  object promotion, tombstone, migration, backup, and restore;
- derived-state rebuild tests proving database/search/cache deletion loses no
  canonical academic truth;
- source-observation fixtures for ambiguous mappings, renamed source objects,
  remote deletion, retries, pagination, stale metadata, rate limits, and
  interrupted sync;
- email fixtures for MIME headers, HTML/text, inline images, calendar
  invitation, thread/reply, duplicate message, shared attachment, PST/MBOX
  source-container coverage, and missing Message-ID;
- course lifecycle fixtures for retakes, cross-semester offerings, changed
  course names, withheld/incomplete/corrected grades, changed deadline,
  attendance correction, transcript replacement, recordings/transcripts;
- offline UI and local-open tests with network disabled;
- Gateway conformance tests for bounded discovery, small-model-friendly
  results/errors, ambiguity, safe refusal, confirmation, and no direct file
  mutation;
- privacy tests proving no private content, secret, raw URL query value, or
  Academic World data can enter logs, fixtures, reports, artifacts, or Git;
- cross-platform filesystem/lock/update/launcher tests;
- performance tests at measured archive sizes.

### 18.3 CI and release gates

CI uses synthetic fixtures only. It validates formatting, schemas, unit/
integration/recovery tests, public-repository scans, license/SBOM checks
when relevant, and reproducible derived-state rebuilds. A release gate
requires:

1. clean source/repository scan;
2. canonical/derived rebuild proof;
3. crash/restore/migration fault-injection evidence;
4. offline source/object UI proof;
5. cross-platform support evidence or explicit supported-platform limits;
6. source-specific connector conformance evidence where a connector ships;
7. license, dependency, signing, and update review;
8. owner review for new canonical schema, permission, source, or migration
   capability.

## 19. Migration from the Docker/Frappe prototype

### 19.1 Preservation boundary

The existing Frappe/Learning/Payments/Studies Hub/Docker runtime is
experimental evidence and must remain intact until a separate migration phase
passes. It contains a local synthetic vertical slice, guarded local-vault
behavior, reports, backups, migration inventories, source audits, and
read-only discovery findings. It must not be reset, cleaned, restructured,
connected to this public repository, or treated as a disposable test fixture.

Docker-managed MariaDB and Redis internals are not ordinary project folders
and must not be copied for visual folder purity. The existing logical
application backup and its recorded manifests/hashes are recovery evidence.
Any future extraction from prototype state must use a read-only export/
adapter and a declared schema, not a raw database dump promoted to canonical
Academic World.

### 19.2 Migration strategy

A future prototype migration must be incremental, non-destructive, and
evidence-driven:

1. inventory source directories, Git state, databases, volumes, configs,
   vault files, reports, backups, and uncommitted changes;
2. classify each item as canonical candidate, derived runtime, source code,
   experimental evidence, private data, or out of scope;
3. write a migration plan and a public-safe synthetic rehearsal before moving
   real content;
4. create/verify independent backups and object/file manifests;
5. build a read-only import adapter that maps prototype entities to proposed
   Core records without rewriting source;
6. run on a synthetic copy, inspect identity/provenance/object differences,
   rebuild derived state, and verify local opening/offline behavior;
7. run a separately approved real-data migration inside a staged destination,
   preserving original files and old runtime intact;
8. compare inventories, hashes, content objects, source/review facts, and
   browser-visible behavior;
9. keep the old prototype read-only and recoverable until acceptance gates,
   independent backup checks, and owner sign-off pass;
10. deprecate only selected runtime components after the new system proves
    parity for the agreed scope.

No data may be lost merely because the old prototype expresses it as a Frappe
DocType or a Docker volume. If a prototype field has no safe target
representation, preserve it as a source/export observation and mark it for
review; do not silently coerce or drop it.

### 19.3 Prototype disposition

| Prototype element | Future disposition |
|---|---|
| Synthetic vertical slice | Preserve as regression evidence and a fixture-design reference. Recreate only with public-safe synthetic data in the new test suite. |
| Studies Hub source | Preserve unchanged as evidence. Reuse concepts/code only after license/provenance and Core-boundary review. |
| Frappe/Learning/Payments source | Preserve exact known source references. Do not vendor or modify in this planning phase. |
| Docker compose/runtime | Preserve until a no-Docker replacement passes all agreed acceptance gates. Never delete engine state merely after a successful UI demonstration. |
| MariaDB/Redis state | Runtime-derived unless a future export maps required facts to canonical records. Back up and retain as prototype recovery evidence. |
| Academic Vault/Notes/reports/backups | Private user-owned evidence. Never push to this repository; migrate only through separate approved preservation work. |
| Graphify artifacts | Retain locally as derived code/document navigation evidence; regenerate from public-safe code in a future source repository as useful. |

## 20. Edge-case constitution

The following cases must have an explicit representation, operation policy,
recovery behavior, and synthetic test. They are architecture constraints, not
a future bug list.

### 20.1 Identity, course, and source cases

- The same subject appears under three source names/codes: preserve three
  source identities; require evidence/review before one canonical mapping.
- Two different subjects have similar titles: remain separate unless
  deterministic evidence or explicit user decision links them.
- A course is renamed mid-semester: retain old source title/version and a
  rename observation; do not change canonical identity merely from a label.
- A course is retaken: create separate attempt and grade/attendance/deadline
  context while retaining any same canonical course relationship.
- A cross-semester course, split offering, section change, or transfer:
  preserve one/many offering relation and source-specific scope.
- Institution merger, rebrand, portal replacement, degree-plan change, or
  program code change: retain historic institution/program aliases and
  effective dates without rewriting history.
- A source stable ID is absent, recycled, or duplicated by a bad importer:
  namespace by source/account/scope, retain evidence, quarantine collision,
  and require review.
- A university account or Teams workspace disappears after graduation:
  record source availability/tombstone; retain local objects and observations.

### 20.2 File, media, and evidence cases

- The same PDF appears in Moodle and Teams: one object hash and two source
  observations/relations.
- Same filename but different bytes: distinct content objects/versions;
  never overwrite by name.
- Lecturer replaces a file: preserve older verified version, record new
  source observation and current-version relation.
- Source deletion/unavailability: do not delete local evidence.
- Corrupted local object: retain recovery evidence, quarantine copy if
  needed, detect hash failure, and restore only from verified backup/source.
- Partial download, interrupted stream, source-side changed content, or
  lost acknowledgement: stage separately, use operation idempotency, and
  promote only verified complete bytes.
- Very large recording, archive, PST, scan, PDF, or video: lazy/local stream,
  resumable policy where supported, no in-memory whole-file requirement.
- Recording without transcript, transcript without recording, multiple
  recordings per lecture, and several transcript versions: explicit
  relationships and provenance, not a nullable one-to-one assumption.
- Raw source export contains unsafe paths, nested archives, malformed MIME,
  unsupported codec, or malicious document content: preserve only under
  quarantine/inspection policy; never execute or follow embedded instructions.

### 20.3 Calendar, time, academic-state cases

- Conflicting deadlines: preserve each source observation and show conflict/
  review rather than choose by source priority silently.
- APU/source timezone versus local device timezone, DST, date-only source
  values, clock skew, late publication, recurring events, cancelled lectures,
  changed rooms, rescheduled exams, and recurring class exceptions: retain
  source-local time facts, timezone/precision, and source update history.
- Attendance correction, retroactive grade correction, withheld grade,
  incomplete result, transcript replacement, and delayed result: later
  source observation/version; preserve earlier observed evidence.
- Exam schedule says none, later appears, then changes: model a source
  observation lifecycle, not a boolean approximation.
- Calendar invitation is related to email and a course, but not proof that a
  meeting occurred or attendance was recorded.

### 20.4 Email and correspondence cases

- One email belongs to multiple courses, an issue, and a project: one
  canonical message plus relations.
- Shared attachment reused by many messages: one content object plus
  message-part relations.
- Inline images/content IDs, multipart alternatives, nested forwarded mail,
  missing Message-ID, duplicate mail in several folders, moved mail, and
  read/unread differences: retain raw MIME/container and explicit
  observation/import identity.
- Very large PST/MBOX, incomplete export, mailbox disabled, provider
  retention policy, and source folder loss: preserve coverage manifest and
  original container; do not claim a partial export is a complete archive.

### 20.5 Filesystem, update, and access cases

- Unicode, Windows-invalid names, case collisions, long/deep paths,
  reparse/symlink escape, external SSD removal, cloud placeholder, and
  cross-platform copy: Core-generated safe paths plus preserved original
  names and integrity verification.
- Moving Studies, opening on another OS, opening a copied workspace, stale
  location configuration, or removable media: workspace identity/lineage,
  relocation receipt, one-writer policy, and explicit fork/repair choice.
- No internet, missing Hermes, missing derived database, missing preview,
  fresh rebuild, old app/newer workspace, migration failure, interrupted
  write, corrupted index, partial backup, or simultaneous UI/AI access:
  local-first/read-only/recovery paths must remain viable.

## 21. Proposed implementation phases

This sequence is a plan, not permission to begin implementation. Each phase
has an explicit completion gate; later phases may not smuggle in unresolved
authority, privacy, licensing, or migration decisions.

### Phase 0 — Authority, evidence, and owner review

- **Objective:** review this draft, establish the first owner-approved
  architecture freeze, and protect private/prototype evidence.
- **Prerequisites:** this plan pushed and independently reviewed.
- **Deliverables:** amended in-place plan, decision log, public/private
  boundary, no-implementation approval record.
- **Invariants:** Academic World authority, Hermes independence, no private
  Git data, no real synchronization.
- **Tests:** plan consistency audit and staged-content privacy scan.
- **Completion gate:** explicit owner approval of the selected frozen
  decisions.
- **Rollback/recovery:** retain this draft and prior commits; no data changes.
- **Depends on later decisions:** none; it resolves their authority.

### Phase 1 — Public repository and vendor baseline

- **Objective:** establish a clean source-only repository, CI foundation, and
  vendor decision process without importing upstream source yet.
- **Prerequisites:** Phase 0 freeze of repository boundary and licensing
  review scope.
- **Deliverables:** defensive ignores, contribution/security policy,
  public-safe synthetic-fixture rules, vendor provenance template, CI
  privacy/lint baseline.
- **Invariants:** no Academic World, secrets, private reports, or runtime
  state in Git.
- **Tests:** staged-content and fixture scans; fresh clone verification.
- **Completion gate:** a clean public repository audit.
- **Rollback/recovery:** revert source-only commits; no private data involved.
- **Dependencies:** vendor import still waits for runtime/framework decision.

### Phase 2 — Canonical Academic World schema

- **Objective:** specify/implement the smallest schema and filesystem contract
  needed to represent identity, object, provenance, relation, review, and
  journal truth.
- **Prerequisites:** Phase 0 approval of canonical/derived rules.
- **Deliverables:** versioned schemas, canonical serializer/parser,
  root/object/entity/relationship manifests, readable cards, synthetic golden
  workspaces.
- **Invariants:** readable durable truth, stable IDs, paths not identity,
  unknown-field preservation, source/personal/test separation.
- **Tests:** schema round trip, malformed input, relation/ID rules, cross-OS
  naming, object-hash verification.
- **Completion gate:** a complete synthetic workspace survives a parser and
  direct filesystem inspection.
- **Rollback/recovery:** schemas/data only in isolated synthetic roots until
  owner approves production data migration.
- **Dependencies:** supplies Core, app, Gateway, and migration work.

### Phase 3 — Deterministic Studies Core

- **Objective:** build the headless Core for identity, object store, safe
  writes, journals, review, and recovery.
- **Prerequisites:** Phase 2 schema and Core/runtime boundary selection.
- **Deliverables:** Core library/CLI/API, operation receipts, one-writer
  coordination, staging/commit protocol, health/doctor, source observation
  primitives.
- **Invariants:** Core-only canonical write authority; AI/UI have no bypass.
- **Tests:** mutation/idempotency/crash/fault/recovery and object dedup tests.
- **Completion gate:** validated pre/post state recovery across all Core
  operation boundaries.
- **Rollback/recovery:** synthetic workspace snapshots and Core operation
  journal recovery.
- **Dependencies:** derived index, app, adapters, Gateway.

### Phase 4 — Derived index, search, and local media

- **Objective:** add rebuildable local database/search/previews without a
  second authority.
- **Prerequisites:** working Phase 3 Core and canonical fixtures.
- **Deliverables:** embedded derived database, rebuild command, local search,
  extraction pipeline, preview/large-object policy.
- **Invariants:** deletion/rebuild loses no canonical data or relation.
- **Tests:** full rebuild, stale/partial index, extracted-text invalidation,
  large-media local-open, privacy namespace tests.
- **Completion gate:** independent clean rebuild equals expected query/
  relationship results.
- **Rollback/recovery:** discard/rebuild derived state only.
- **Dependencies:** native UI, Gateway retrieval, archive usability.

### Phase 5 — Native Studies App foundation

- **Objective:** create the real app over the Core, not a second data model.
- **Prerequisites:** approved UI/runtime choice and Phase 3/4 contract.
- **Deliverables:** workspace selection, dashboard, course/offering/resource
  browser, provenance/review/health surfaces, local-open and offline states.
- **Invariants:** app calls Core; no hidden app database; origin/freshness
  visible.
- **Tests:** offline UI, app-to-Core operations, accessibility, file-open
  safety, no-AI operation.
- **Completion gate:** a synthetic Academic World is fully usable with
  network/AI disabled.
- **Rollback/recovery:** UI failure leaves Academic World unchanged.
- **Dependencies:** no-Docker packaging and future source views.

### Phase 6 — No-Docker runtime and launcher

- **Objective:** make Launch Studies start/open/shut down a local workspace
  without user-managed services.
- **Prerequisites:** Phase 5 app and selected runtime topology.
- **Deliverables:** installer/portable launcher prototype, lifecycle,
  health/repair UX, local secret boundary, update/rollback scaffolding.
- **Invariants:** no Docker requirement; one writer; clear failure state.
- **Tests:** first run, restart, crash, update rollback, external path, and
  offline launch on target OSs.
- **Completion gate:** normal user flow requires no terminal, Docker, or
  database knowledge.
- **Rollback/recovery:** app binaries/derived state rollback; Academic World
  remains untouched without a verified migration.
- **Dependencies:** replaces, but does not yet delete, prototype runtime.

### Phase 7 — University source adapters: read-only observations

- **Objective:** add source-specific read-only adapter framework and one
  limited authorized discovery proof at a time.
- **Prerequisites:** Phase 3 Core, Phase 6 runtime, source-specific consent,
  adapter threat/permission design.
- **Deliverables:** adapter interface, source registry, observation/rate/
  pagination/retry policy, review queue, isolated synthetic/live test plan.
- **Invariants:** no browser-session reuse, no remote writes, no automatic
  canonical merge.
- **Tests:** fixture adapters, denied/expired credential, cursor/tombstone,
  rate-limit/backoff, source policy tests.
- **Completion gate:** one approved source proves a bounded, journalled,
  read-only observation path without privacy regression.
- **Rollback/recovery:** disable adapter; retain local observations/
  originals and authorization audit.
- **Dependencies:** source-specific connector gates remain independent.

### Phase 8 — University email archival

- **Objective:** build complete local email archive ingestion and views.
- **Prerequisites:** Phase 3 object/relation Core, explicit source/export
  authorization, privacy/retention approval.
- **Deliverables:** EML/PST/MBOX/MSG source-container pipeline, message/
  attachment/thread/calendar model, coverage manifest, search/index views.
- **Invariants:** one canonical message/object, raw originals preserved,
  no remote mail mutation, local-only privacy.
- **Tests:** MIME/inline/thread/calendar/duplicate/large-export fixtures and
  account-closure/readability simulation.
- **Completion gate:** a synthetic full mailbox archive is portable,
  searchable, and linked to several courses without copies.
- **Rollback/recovery:** staged archival import, immutable original
  containers, journalled cancellation/retry.
- **Dependencies:** source adapter/export selection and Gateway retrieval.

### Phase 9 — Offline local university corpus

- **Objective:** promote approved observations/downloads into local course
  archives through reconciliation review.
- **Prerequisites:** Phase 7 and applicable Phase 8 output.
- **Deliverables:** institution/course/attempt views, resource/assessment/
  attendance/grade/calendar representations, local media/recording handling.
- **Invariants:** no title-only merge; no source deletion of local evidence;
  personal/source separation.
- **Tests:** source replacement, retake, renamed offering, deadline
  conflict, offline browser/app proof.
- **Completion gate:** owner-approved small real-data pilot with source
  provenance and offline verification.
- **Rollback/recovery:** leave source staged; preserve original artifacts and
  review records; no remote changes.
- **Dependencies:** each service must meet its own authorization/evidence gate.

### Phase 10 — External Courses

- **Objective:** support provider and fully local learning through the shared
  model.
- **Prerequisites:** Phase 2/3/4 model stability.
- **Deliverables:** provider/self-study course views, curriculum/book/
  certificate records, optional progress and evidence structure.
- **Invariants:** no university-only schema assumptions or fake grades.
- **Tests:** local-only course, provider course, shared resource, transfer/
  rename scenarios.
- **Completion gate:** external courses work completely offline without
  university connector configuration.
- **Rollback/recovery:** isolated canonical records and standard snapshots.
- **Dependencies:** optional source adapters only after specific approval.

### Phase 11 — Islamic Studies

- **Objective:** add the first-class Islamic Studies domain without
  institution assumptions.
- **Prerequisites:** Phase 2/3 identity/evidence/notes model.
- **Deliverables:** curriculum/subject/book/teacher/reading/memorization/
  revision structures and UI vocabulary.
- **Invariants:** no content population by architecture work; separate
  personal/source origin and citations.
- **Tests:** local curriculum/reading/note/progress fixtures, Unicode/Arabic
  search and cross-platform path tests.
- **Completion gate:** a synthetic domain stays coherent without pretending
  it is a university.
- **Rollback/recovery:** standard canonical snapshot/derived rebuild.
- **Dependencies:** native UI, search, Gateway retrieval.

### Phase 12 — Studies Gateway and Hermes conformance

- **Objective:** publish/test one model-agnostic typed contract for Hermes
  and any future AI.
- **Prerequisites:** stable Core operations and bounded index/query support.
- **Deliverables:** capability discovery, schemas, examples, result/error
  contract, approval/risk policy, 1B-model test harness.
- **Invariants:** app remains complete without Hermes; no direct model
  filesystem/db/write path.
- **Tests:** constrained-model safe retrieval, ambiguity, refusal,
  confirmation, idempotency, prompt-injection resistance.
- **Completion gate:** a small-model simulation completes representative
  bounded tasks via Gateway without implementation knowledge.
- **Rollback/recovery:** disable Gateway client layer; Core/Academic World
  remains fully usable.
- **Dependencies:** no AI provider lock-in.

### Phase 13 — Cross-platform, security, and scale hardening

- **Objective:** prove runtime, workspace, data, and update behavior on
  Windows, macOS, and Linux at target scale.
- **Prerequisites:** Phases 4-6 and selected functionality.
- **Deliverables:** platform packages, locking/path/media tests, SBOM,
  signing/update plan, performance data, redacted diagnostics.
- **Invariants:** semantic identity/provenance/relationship portability.
- **Tests:** cross-platform fixtures, removable/cloud storage, corruption,
  performance, privacy, update/rollback.
- **Completion gate:** supported-platform matrix and documented limits.
- **Rollback/recovery:** signed prior app + verified snapshots and
  migration recovery.
- **Dependencies:** release gate and prototype deprecation.

### Phase 14 — Verified migration from prototype

- **Objective:** migrate approved private/prototype content only after the
  new product proves its target capabilities.
- **Prerequisites:** Phases 2-6 plus owner-approved scope and independent
  backups.
- **Deliverables:** read-only prototype importer, mapping report, inventory/
  hash comparison, user acceptance evidence, deprecation plan.
- **Invariants:** preserve original prototype, user files, reports, source
  evidence, uncommitted Git work, and Docker recovery path.
- **Tests:** synthetic rehearsal, staged real-data pilot, compare/rebuild/
  offline checks, rollback drill.
- **Completion gate:** owner verifies complete new root and no data loss;
  old prototype still recoverable.
- **Rollback/recovery:** keep old root/runtime read-only until independent
  acceptance and backup retention period pass.
- **Dependencies:** final runtime/vendor decision and personal data approval.

### Phase 15 — Long-term validation and release

- **Objective:** prove decades-long retention, recoverability, and
  maintainable release behavior.
- **Prerequisites:** all selected feature domains and migrations complete.
- **Deliverables:** release criteria, archival/export procedure, full
  recovery drill, support/diagnostic policy, maintenance/version policy.
- **Invariants:** readable Academic World, rebuildable derived state,
  no-Hermes operation, no-private-Git, no hidden source authority.
- **Tests:** full synthetic archive/rebuild/restore, old-version/newer-
  workspace behavior, account-closure scenario, large corpus performance.
- **Completion gate:** owner release review and independent backup/restore
  proof.
- **Rollback/recovery:** retain release artifacts, schema compatibility
  policy, verified snapshots, and supported read-only recovery.
- **Dependencies:** ongoing source/vendor/security review.

### 21.1 Task queue philosophy

Implementation work is carried out as small, evidence-scoped tasks. Each task
declares:

- the authority/data origin it may read or write;
- preconditions, expected files/objects, and idempotency key if mutating;
- expected canonical/derived output and verification;
- privacy/secrets policy and public-repository effect;
- tests, rollback/recovery route, and stop conditions;
- whether user/admin authorization is required.

Tasks never expand a source scope merely because nearby data is visible. A
blocked connector or consent flow records a blocker and continues with
independent local work. Queues are explicit, rate-aware, pauseable,
idempotent, and observable; they never turn a source discovery into a mass
sync by accident.

## 22. Acceptance criteria

Studies is not ready for a production/private-data migration until repeatable
synthetic evidence demonstrates all applicable criteria below:

1. Academic World is understandable in a normal file browser and text editor
   without an opaque database or the native app.
2. Every meaningful entity has a stable product ID that survives supported
   renames, moves, source-title changes, index rebuilds, and app updates.
3. A canonical course, offering, and attempt remain distinct; retakes and
   cross-semester offerings do not collapse grades, attendance, or deadlines.
4. The same byte-identical object from two sources is preserved once with two
   source observations; same-name different bytes remain distinct versions.
5. A source replacement preserves the old verified object and records a
   later version relation; a remote deletion does not delete local evidence.
6. Original files, mail, provider exports, recordings, transcripts,
   attachments, personal notes, and source observations retain provenance and
   are not silently overwritten.
7. Source-derived, personal, test, normalized, derived, and uncertain data
   origins remain visible in filesystem records, UI, search, Gateway results,
   and logs.
8. Database/search/vector/preview/cache deletion loses no canonical fact,
   object, relation, provenance, review decision, or journal history; a
   deterministic rebuild restores the expected query result set.
9. An absent/corrupt derived index enters an explicit rebuild/recovery state,
   not a data-loss or hidden-stale state.
10. The Core, not UI/AI/Frappe tables/source portal, owns canonical ID,
    relation, object placement, and material write validation.
11. The native app can operate entirely with AI, Hermes, and network
    unavailable.
12. Hermes can be removed without impacting local course/archive/search/
    backup functionality.
13. Any AI uses one typed Studies Gateway; no AI receives a generic direct
    canonical filesystem/database or secret write path.
14. A constrained approximately one-billion-parameter model can use bounded
    capability discovery, resolve friendly references through the Core, ask
    safe clarifications, and receive a verified result without scanning the
    workspace or manufacturing IDs.
15. Gateway errors include human-readable reason, relevant candidates, and a
    safe next action.
16. Material Gateway operations produce a preview and required approval
    before commit; retries with the same operation ID cannot duplicate work.
17. The Core's staged/journalled write protocol recovers to a valid complete
    pre- or post-operation state under fault injection.
18. One writer is coordinated across UI/Core/Gateway access; stale/parallel
    writers cannot silently overwrite an academic record.
19. Manual conflict, malformed record, duplicate ID, and source collision
    cases surface explicit review data without silent last-writer-wins.
20. A backup captures canonical objects/manifests/journals/relations and
    validates inventory/hashes before it is called usable.
21. Restore supports inspect/compare/replace/selected recovery/fork
    semantics, preserves current data until confirmation, and validates after
    restore.
22. A migration creates a verified pre-migration snapshot, preserves
    meaningful data/unknown safe fields, and stops for recovery on anomaly.
23. An old app cannot silently downgrade a newer workspace.
24. Local search filters source/freshness/data origin and opens verified local
    resources without network access.
25. Text extraction, preview, OCR, transcript, and media derivative failures
    never alter/remove originals or claim unreviewed text is source truth.
26. Large recordings/archives are opened/read lazily and do not require
    loading the entire corpus in memory.
27. A canonical email is preserved once, retains original MIME/container
    evidence, headers, body, attachments, thread/calendar relations, and can
    link to several courses without copies.
28. A partial/large/moved mailbox export has an explicit coverage/limitation
    manifest and never claims complete archival coverage without evidence.
29. A connector cannot send, edit, submit, upload, alter attendance/grade,
    change a calendar event, or reuse browser sessions.
30. Every connector is read-only, least-privilege, source-scoped, rate-aware,
    idempotent, pauseable, and journalled, with explicit authorization
    evidence.
31. A title/code resemblance cannot auto-merge source courses; a mapping
    requires evidence/review and retains all source identities.
32. APU/other institution terms, human year/semester views, source codes,
    offering/attempts, timezone facts, and graduation archive state coexist
    without false equivalence.
33. Attendance corrections, withheld/incomplete/corrected grades, revised
    transcripts, conflicting deadlines, recurring/cancelled events, and
    source disappearance retain their original and later observed history.
34. External Courses and Islamic Studies use the same Core/evidence/object
    model without being forced into university-only fields.
35. Unicode, Windows-invalid names, long paths, case differences, external
    drives, OneDrive/cloud conflict copies, reparse points, and cross-OS
    moves are handled by tested Core policy.
36. Launch Studies starts and shuts down a healthy local workspace without
    Docker, Bench, MariaDB, Redis, port, or terminal knowledge from the user.
37. Windows, macOS, and Linux retain the same canonical semantics; platform
    differences and unsupported features are explicit.
38. A source repository clone/CI/release has no Academic World, real
    university content, secrets, tokens, raw query-bearing URLs, private
    reports, or backups.
39. Any vendor source import records source, exact revision/digest, license,
    notices, provenance, modification policy, and compliance review before
    commit.
40. The current prototype stays recoverable until a separately accepted
    migration proves preservation, offline behavior, backups, and user
    acceptance for the agreed scope.

## 23. Deferred decisions requiring owner review

These choices are deliberately unresolved. They must not be decided by a
convenient implementation default:

1. **Framework/runtime:** select among a product-owned runtime (Option E), a
   Core-separated Frappe application (Option D), or a limited Frappe/Learning
   continuity role (Options A/B) after feasibility evidence. Option C vendor
   control remains possible but unproven.
2. **Vendor strategy:** whether to vendor Frappe/Learning at all, which exact
   snapshot, whether upstream security merges are expected, and what legal
   obligations are acceptable.
3. **Core technology/UI/IPC:** language, desktop shell, in-process versus
   local service boundary, installer/updater, and local secret-store
   mechanism.
4. **Canonical serialization:** exact JSON/Markdown schema, relation
   syntax, human-edit policy, versioning, extension/unknown-field rules, and
   object manifest structure.
5. **Workspace copy/fork/merge semantics:** workspace/device IDs, external
   drive/cloud folder behavior, lock lease/fencing mechanism, and future
   multi-device policy.
6. **Encryption:** whether it is offered, default posture, key lifecycle,
   recovery, backup, cross-platform behavior, and AI boundary.
7. **Email acquisition:** preferred supported acquisition/export route for
   the user's university account(s), preservation coverage expectation,
   folder/category/read-state model, and exact PST/MBOX/EML handling.
8. **Connector authorization:** which sources are worth integrating; lawful
   permission scopes; admin/user consent; source policies; data retention;
   and whether any connector progresses beyond manual/inbound discovery.
9. **Institution terminology:** exact user-approved APU and Virtual
   University human folder/card structure based on private evidence,
   including degree/year/semester labels and policies/appeals retention.
10. **Retention/destruction:** legal/personal retention periods, optional
    secure deletion limits, export/redaction policy, and whether old source
    versions can ever be user-purged.
11. **Performance targets:** supported archive scale, hardware baseline,
    index strategy, media/transcoding policy, and latency budgets.
12. **Public release posture:** open-source/private distribution intent,
    signing, SBOM, support, compliance, and vendor-source publication plan.

## 24. Risk register

| Risk | Consequence | Required control/gate |
|---|---|---|
| Frappe/Learning becomes database authority by convenience | Academic archive trapped in runtime state. | Core/Academic World conformance and rebuild test before any long-term adoption. |
| AGPL/vendor obligations misunderstood | Incompatible release or compliance exposure. | Competent license review before any source import/combined distribution. |
| Browser session reuse or over-broad connector | Security/privacy breach or remote university change. | Provider-supported consent only; read-only adapter policy; no cookie/token extraction. |
| Title-only course merge | Incorrect course, grade, assignment, or file relationship. | Strong key/review gate and preserved candidate evidence. |
| Remote deletion overwrites archive | Irreplaceable local academic history lost. | Tombstones/observations; no automatic local deletion. |
| Synced/cloud folder conflict | Corrupt/duplicated canonical records. | One-writer coordination, revision hashes, conflict review, explicit cloud policy. |
| Interrupted import/write/migration | Partial or misleading archive. | Staging, journals, idempotency, fault injection, verified snapshots. |
| Large files/mail archives exhaust device | Product unusable or unsafe failure. | Streaming/lazy loading, quotas, preflight, cancellable derived work. |
| Private data enters Git/logs/fixtures | Permanent privacy disclosure. | Defensive ignore, staged scan, synthetic fixtures, redacted diagnostics/CI gate. |
| AI prompt injection or hallucinated relationship | Unauthorized/incorrect canonical mutation. | Typed Gateway, Core validation, review/approval, no direct write. |
| Prototype data migration loses hidden facts | Loss of existing work or irreproducible result. | Read-only adapter, inventory/hash comparisons, staged pilot, old runtime retention. |
| Old/new version incompatibility | Silent downgrade/corruption. | Schema version gate, read-only refusal, verified migration/rollback. |
| Source account closes before archive | Missing future evidence. | Owner-approved email/archive plan, coverage manifests, proactive but authorized export. |
| No-Docker goal degrades into hidden operations burden | Product unusable for the owner. | Launch Studies UX test; runtime process/supervision proof on each platform. |

## 25. Final target architecture

The target is a user-owned durable Academic World and a deterministic
product-owned Core. It is intentionally independent of both Hermes and the
current prototype:

~~~
                                 USER
                      ┌───────────┴───────────┐
                      │                       │
                Native Studies App      Any AI / Hermes
                      │                       │
                      │                 Studies Gateway
                      │                       │
                      └───────────┬───────────┘
                                  ▼
                    Deterministic Studies Core
          identity · provenance · objects · review · journal
          import · recovery · migrations · indexes · safe writes
                                  ▼
                            Academic World
  original objects · readable cards · manifests · relations · audit history
                                  │
              ┌───────────────────┼───────────────────┐
              ▼                   ▼                   ▼
          derived DB          local search        previews/cache
        rebuildable           rebuildable          rebuildable
~~~

Frappe, Frappe Learning, a desktop shell, an embedded database, a source
adapter, Graphify, Hermes, a model provider, and any future index are
implementation components or clients. They can be replaced or removed only
after a deliberate migration/compatibility path, but none is allowed to
become a hidden second source of academic truth.

The application should remain complete with no internet, no university
account, no AI, and no derived index. If a future implementation selects
Frappe, its local runtime may be needed to run that implementation's interface;
it must never be the sole holder of academic truth. In every implementation,
the absence of the app or runtime cannot erase the archive: a person can still
browse preserved originals, readable cards, source provenance, relationships,
personal notes, and verified backups; the Core can
rebuild the application view when software becomes available.

## 26. Future review loop and governance

This file is authoritative draft status only. It becomes frozen only after
the owner explicitly authorizes an architecture freeze.

For each future amendment:

1. fetch/check the current repository state;
2. read the entire current STUDIES_MASTER_PLAN.md;
3. inspect the requested amendment and current evidence;
4. reconcile all affected sections, tables, requirements, risks, phases, and
   acceptance criteria in place;
5. preserve compatible hard requirements and explicitly amend incompatible
   ones instead of appending contradictory text;
6. run a full contradiction audit for authority, database, Hermes, UI,
   Frappe/Learning, vendor strategy, Docker/runtime, filesystem, email,
   deduplication, IDs, source mappings, AI permissions, backups, migration,
   and platform claims;
7. scan staged changes for private data/secrets;
8. commit/push only the intended public-safe files and verify remote file
   contents/commit; then
9. stop again for owner review.

No implementation may start merely because the plan is published. The owner
and reviewer decide when the draft is sufficiently amended to freeze, and
only then authorize the first implementation phase.

## Closing principle

If an academic fact, source file, relationship, correction, uncertainty, or
historical event matters years later, Studies must either preserve and explain
it through Academic World or state clearly that it is unknown/unavailable.
It must never quietly guess, hide it in a disposable database, or erase it
because a current app, AI, source portal, or account no longer exists.
