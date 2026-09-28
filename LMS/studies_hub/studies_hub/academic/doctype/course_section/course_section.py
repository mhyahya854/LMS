import frappe
from frappe import _
from frappe.model.document import Document


class CourseSection(Document):
	def validate(self):
		if self.data_origin == "Personal" and self.source_course_mapping:
			frappe.throw(_("Personal sections cannot carry an external course mapping."), frappe.ValidationError)
