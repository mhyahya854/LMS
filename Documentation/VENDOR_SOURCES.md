# Local Vendor Sources

The following local working trees are intentionally excluded from the outer
Studies repository. They preserve a continuity runtime while vendor strategy,
license obligations, and future bootstrap design remain owner decisions.

| Relative path | Upstream/source | Observed revision | Status |
| --- | --- | --- | --- |
| `LMS/frappe-lms/` | Frappe Learning | `2ee6156` (`v2.63.0`) | Clean detached checkout. |
| `Vendor/Frappe Learning/Root Checkout 2026-09-27/` | Frappe Learning | `2ee6156` | Clean byte-identical preserved root checkout. |
| `LMS/frappe_docker/` | Frappe Docker | `3d0a0e5` | Clean `main` checkout. |
| `LMS/runtime/bench/frappe-bench/apps/frappe/` | Frappe Framework | `012667b` (`version-16`) | Local modifications exist; not changed by reconciliation. |
| `LMS/runtime/bench/frappe-bench/apps/lms/` | Frappe Learning runtime checkout | `2ee6156` | Runtime working tree has local generated changes; not changed by reconciliation. |
| `LMS/runtime/bench/frappe-bench/apps/payments/` | Frappe Payments | `cca07d9` (`version-16`) | Clean checkout. |

No vendor source is staged by the outer repository. Any future source import
requires license, provenance, modification-policy, privacy, and size review.
