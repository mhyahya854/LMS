import re

import frappe
from frappe import _
from frappe.model.document import Document

from studies_hub.vault.storage import safe_vault_path, vault_root


class AcademicFile(Document):
	def validate(self):
		if self.data_origin == "Personal" and any(
			(self.source_course_mapping, self.source_system, self.external_object_id, self.source_url)
		):
			frappe.throw(
				_("Personal files cannot carry external source identity fields."),
				frappe.ValidationError,
			)
		if not re.fullmatch(r"[0-9a-f]{64}", self.sha256 or ""):
			frappe.throw(_("SHA-256 must contain 64 lowercase hexadecimal characters."), frappe.ValidationError)
		try:
			path = safe_vault_path(vault_root(), self.vault_relative_path)
		except (OSError, ValueError) as exc:
			frappe.throw(_("Invalid vault path: {0}").format(exc), frappe.ValidationError)
		if not path.is_file():
			frappe.throw(_("The local file is missing from the configured academic vault."), frappe.ValidationError)
		if path.stat().st_size != self.byte_size:
			frappe.throw(_("The local file size no longer matches its registered metadata."), frappe.ValidationError)
