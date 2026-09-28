import frappe
from frappe.tests.utils import FrappeTestCase

from studies_hub.academic.api import get_course_view


class TestLocalCourseView(FrappeTestCase):
	def test_course_and_source_mappings_load_from_local_records(self):
		course = frappe.get_doc(
			{
				"doctype": "Canonical Course",
				"title": frappe.generate_hash(length=8),
				"data_origin": "Test data",
			}
		).insert(ignore_permissions=True)
		frappe.get_doc(
			{
				"doctype": "External Course Mapping",
				"canonical_course": course.name,
				"source_system": "Microsoft Teams",
				"external_course_id": "TEST-" + frappe.generate_hash(length=8),
				"sync_state": "Local only",
			}
		).insert(ignore_permissions=True)

		result = get_course_view(course.name)["courses"][0]

		self.assertEqual(result.name, course.name)
		self.assertEqual(len(result.mappings), 1)
		self.assertEqual(result.mappings[0].sync_state, "Local only")
