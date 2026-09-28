import os
import tempfile
from pathlib import Path

import frappe
from frappe.tests.utils import FrappeTestCase

from studies_hub.academic.api import get_course_view
from studies_hub.vault.storage import safe_vault_path, store_bytes


class TestAcademicVerticalSlice(FrappeTestCase):
	def setUp(self):
		super().setUp()
		self.original_user = frappe.session.user
		frappe.set_user("Administrator")
		self.course = frappe.get_doc(
			{
				"doctype": "Canonical Course",
				"title": frappe.generate_hash(length=8),
				"institution": "Synthetic Example University",
				"data_origin": "Test data",
			}
		).insert(ignore_permissions=True)
		self.vault = tempfile.TemporaryDirectory()
		self.old_vault_env = os.environ.get("STUDIES_HUB_VAULT_ROOT")
		os.environ["STUDIES_HUB_VAULT_ROOT"] = self.vault.name

	def tearDown(self):
		if self.old_vault_env is None:
			os.environ.pop("STUDIES_HUB_VAULT_ROOT", None)
		else:
			os.environ["STUDIES_HUB_VAULT_ROOT"] = self.old_vault_env
		self.vault.cleanup()
		frappe.set_user(self.original_user)
		super().tearDown()

	def test_multiple_sources_and_local_resource_are_available_offline(self):
		mappings = []
		for source, external_id in (
			("APSpace", "TEST-APSPACE-" + frappe.generate_hash(length=8)),
			("Moodle", "TEST-MOODLE-" + frappe.generate_hash(length=8)),
			("Microsoft Teams", "TEST-TEAMS-" + frappe.generate_hash(length=8)),
		):
			mappings.append(
				frappe.get_doc(
					{
						"doctype": "External Course Mapping",
						"canonical_course": self.course.name,
						"source_system": source,
						"external_course_id": external_id,
						"sync_state": "Unavailable",
						"provenance_note": "Synthetic test mapping; source unavailable and not contacted.",
					}
				).insert(ignore_permissions=True)
			)

		section = frappe.get_doc(
			{
				"doctype": "Course Section",
				"canonical_course": self.course.name,
				"title": "Lecture 01",
				"section_type": "Lecture",
				"data_origin": "Test data",
				"source_course_mapping": mappings[1].name,
			}
		).insert(ignore_permissions=True)
		content = b"TEST DATA - local copy remains usable offline\n"
		stored = store_bytes(content, self.vault.name, ("Test Data", "Computer Systems", "Lecture 01"), "slides.txt")
		resource = frappe.get_doc(
			{
				"doctype": "Academic Resource",
				"canonical_course": self.course.name,
				"course_section": section.name,
				"title": "Lecture 01 slides",
				"resource_type": "Slides",
				"data_origin": "Test data",
				"source_course_mapping": mappings[1].name,
				"source_system": "Moodle",
				"external_object_id": "TEST-MOODLE-SLIDES-01",
				"source_title": "Lecture 01 slides",
				"sync_state": "Unavailable",
			}
		).insert(ignore_permissions=True)
		file_doc = frappe.get_doc(
			{
				"doctype": "Academic File",
				"canonical_course": self.course.name,
				"academic_resource": resource.name,
				"original_filename": stored["original_filename"],
				"vault_relative_path": stored["vault_relative_path"],
				"sha256": stored["sha256"],
				"byte_size": stored["byte_size"],
				"content_type": stored["content_type"],
				"data_origin": "Test data",
				"source_course_mapping": mappings[1].name,
				"source_system": "Moodle",
				"external_object_id": "TEST-MOODLE-SLIDES-01",
			}
		).insert(ignore_permissions=True)

		view = get_course_view(self.course.name)["courses"][0]

		self.assertEqual({mapping.source_system for mapping in view.mappings}, {"APSpace", "Moodle", "Microsoft Teams"})
		self.assertTrue(all(mapping.sync_state == "Unavailable" for mapping in view.mappings))
		self.assertEqual(view.resources[0].data_origin, "Test data")
		self.assertEqual(view.resources[0].sync_state, "Unavailable")
		self.assertEqual(view.resources[0].files[0].name, file_doc.name)
		self.assertEqual(safe_vault_path(self.vault.name, stored["vault_relative_path"]).read_bytes(), content)

	def test_personal_note_stays_separate_from_external_source_records(self):
		personal = frappe.get_doc(
			{
				"doctype": "Academic Resource",
				"canonical_course": self.course.name,
				"title": "My revision note",
				"resource_type": "Personal Note",
				"data_origin": "Personal",
				"content_text": "Review process scheduling.",
			}
		).insert(ignore_permissions=True)
		self.assertEqual(personal.data_origin, "Personal")
		self.assertFalse(personal.source_system)
