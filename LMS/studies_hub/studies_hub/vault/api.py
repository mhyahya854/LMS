import frappe
from frappe import _

from studies_hub.vault.storage import open_vault_file, sha256_file

MAX_INLINE_FILE_BYTES = 32 * 1024 * 1024


@frappe.whitelist()
def open_local_file(file_id):
	if frappe.session.user == "Guest":
		frappe.throw(_("Log in to open local academic files."), frappe.PermissionError)
	file_doc = frappe.get_doc("Academic File", file_id)
	file_doc.check_permission("read")
	try:
		path = open_vault_file(file_doc.vault_relative_path)
	except (OSError, ValueError, RuntimeError) as exc:
		frappe.throw(_("Could not safely open this local file: {0}").format(exc), frappe.ValidationError)
	file_size = path.stat().st_size
	if file_size > MAX_INLINE_FILE_BYTES:
		frappe.throw(
			_("Browser opening is limited to 32 MiB in this prototype; use the local vault copy for larger files."),
			frappe.ValidationError,
		)
	if file_size != file_doc.byte_size:
		frappe.throw(_("This local file changed after registration; re-register it to confirm the new version."), frappe.ValidationError)
	if sha256_file(path) != file_doc.sha256:
		frappe.throw(_("This local file no longer matches its registered SHA-256."), frappe.ValidationError)
	frappe.response["filename"] = file_doc.original_filename
	frappe.response["filecontent"] = path.read_bytes()
	frappe.response["content_type"] = file_doc.content_type or "application/octet-stream"
	frappe.response["display_content_as"] = "inline"
	frappe.response["type"] = "download"
