import frappe
from frappe import _
from frappe.model.document import Document


class AcademicAssignment(Document):
	def validate(self):
		if self.data_origin == "Personal" and any(
			(self.source_course_mapping, self.source_system, self.external_object_id, self.source_url)
		):
			frappe.throw(
				_("Personal assignments cannot carry external source identity fields."),
				frappe.ValidationError,
			)
