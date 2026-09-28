import frappe
from frappe.tests.utils import FrappeTestCase


class TestExternalCourseMapping(FrappeTestCase):
	def setUp(self):
		self.course = frappe.get_doc(
			{
				"doctype": "Canonical Course",
				"title": frappe.generate_hash(length=8),
				"data_origin": "Test data",
			}
		).insert(ignore_permissions=True)

	def test_one_source_identity_cannot_map_to_two_courses(self):
		external_id = "TEST-" + frappe.generate_hash(length=8)
		frappe.get_doc(
			{
				"doctype": "External Course Mapping",
				"canonical_course": self.course.name,
				"source_system": "Moodle",
				"external_course_id": external_id,
			}
		).insert(ignore_permissions=True)
		duplicate = frappe.get_doc(
			{
				"doctype": "External Course Mapping",
				"canonical_course": self.course.name,
				"source_system": "Moodle",
				"external_course_id": external_id,
			}
		)
		with self.assertRaises(frappe.ValidationError):
			duplicate.insert(ignore_permissions=True)
