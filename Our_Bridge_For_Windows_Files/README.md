# Our Bridge For Windows Files

A Windows-native bridge between the user-owned `Academic World/Personal Study/Notes and Studies Legacy/` library and Studies Hub/LMS. This repository is a scaffold only; no background indexing, file movement, upload, or sync runs yet.

## Safety contract

- The user-owned Personal Study tree remains the durable source of truth.
- Initial indexing is read-only and opt-in by root; no automatic deletes, moves, or overwrites.
- Preserve original names and bytes. Identify files by stable IDs plus content hashes, not filenames alone.
- Store references relative to an explicitly configured root where possible; reject paths escaping that root.
- Report ambiguous, unsupported, changed, or inaccessible items instead of guessing.
- Keep parsing adapters separate for PDF, Markdown, TXT, DOCX, PPTX, XLSX, images, audio, video, recordings, transcripts, and university exports.
- Never extract browser cookies, LMS tokens, passwords, or other credentials.

Implementation begins after the local Frappe foundation is available. The first version should inventory metadata and hash files without moving them; each format parser and sync action will be added behind tests and explicit user-visible controls.
