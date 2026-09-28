import frappe
from frappe.tests.utils import FrappeTestCase


class TestAcademicResource(FrappeTestCase):
	def setUp(self):
		self.course = frappe.get_doc(
			{
				"doctype": "Canonical Course",
				"title": frappe.generate_hash(length=8),
				"data_origin": "Test data",
			}
		).insert(ignore_permissions=True)

	def test_personal_note_cannot_claim_external_provenance(self):
		resource = frappe.get_doc(
			{
				"doctype": "Academic Resource",
				"canonical_course": self.course.name,
				"title": "Personal note",
				"resource_type": "Personal Note",
				"data_origin": "Personal",
				"source_system": "Moodle",
			}
		)
		with self.assertRaises(frappe.ValidationError):
			resource.insert(ignore_permissions=True)
