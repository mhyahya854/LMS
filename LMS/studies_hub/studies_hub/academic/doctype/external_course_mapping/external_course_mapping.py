import frappe
from frappe import _
from frappe.model.document import Document


class ExternalCourseMapping(Document):
	def validate(self):
		filters = {"source_system": self.source_system, "external_course_id": self.external_course_id}
		if self.name:
			filters["name"] = ["!=", self.name]
		if frappe.db.exists("External Course Mapping", filters):
			frappe.throw(
				_("This external course ID is already mapped for {0}.").format(self.source_system),
				frappe.ValidationError,
			)
