import json

from studies_hub.vault.storage import store_bytes, vault_root


TEST_NOTE = "TEST DATA — not official university information"


def _source_metadata(source_system, external_id):
	return json.dumps(
		{
			"test_data": True,
			"not_official": True,
			"source_system": source_system,
			"external_object_id": external_id,
			"note": TEST_NOTE,
		},
		ensure_ascii=False,
	)


def _get_or_insert(doctype, filters, values):
	import frappe

	name = frappe.db.get_value(doctype, filters, "name")
	if name:
		return frappe.get_doc(doctype, name)
	return frappe.get_doc({"doctype": doctype, **filters, **values}).insert(ignore_permissions=True)


def seed_demo_data():
	import frappe

	course = _get_or_insert(
		"Canonical Course",
		{"title": "Computer Systems", "data_origin": "Test data"},
		{
			"preferred_short_title": "Computer Systems",
			"institution": "Synthetic Example University",
			"program": "Synthetic Test Program",
			"academic_year": "2026",
			"term": "Demonstration term",
			"status": "Active",
			"description": TEST_NOTE,
		},
	)
	mapping_specs = [
		("APSpace", "TEST-APSPACE-CS-01", "CT017-3-2", "Computing Fundamentals — synthetic APSpace record"),
		("Moodle", "TEST-MOODLE-CS-01", "CT017", "Computer Architecture — synthetic Moodle record"),
		("Microsoft Teams", "TEST-TEAMS-CS-01", "CS-AUTUMN", "Systems Cohort — synthetic Teams record"),
	]
	mappings = {}
	for source, external_id, code, title in mapping_specs:
		mapping = _get_or_insert(
			"External Course Mapping",
			{"source_system": source, "external_course_id": external_id},
			{
				"canonical_course": course.name,
				"external_code": code,
				"external_title": title,
				"sync_state": "Local only",
				"provenance_note": TEST_NOTE + "; simulated identity, never contacted the service.",
				"source_metadata": _source_metadata(source, external_id),
			},
		)
		mappings[source] = mapping

	section = _get_or_insert(
		"Course Section",
		{"canonical_course": course.name, "title": "Lecture 01"},
		{
			"section_type": "Lecture",
			"position": 1,
			"data_origin": "Test data",
			"source_course_mapping": mappings["Moodle"].name,
			"source_metadata": _source_metadata("Moodle", "TEST-MOODLE-CS-01"),
		},
	)

	files = [
		{
			"title": "Lecture 01 slides (test file)",
			"resource_type": "Slides",
			"filename": "Lecture 01 slides.txt",
			"content": (
				TEST_NOTE
				+ "\n\nComputer Systems — Lecture 01\nPlaceholder slide 1: systems are represented here for a local-first test.\n"
			),
			"source": "Moodle",
			"external_object_id": "TEST-MOODLE-RESOURCE-SLIDES-01",
		},
		{
			"title": "Lecture 01 transcript (test file)",
			"resource_type": "Transcript",
			"filename": "Lecture 01 transcript.txt",
			"content": (
				TEST_NOTE
				+ "\n\nInstructor: This is a harmless synthetic transcript used to verify local file access.\n"
			),
			"source": "Microsoft Teams",
			"external_object_id": "TEST-TEAMS-TRANSCRIPT-01",
		},
	]
	root = vault_root()
	for spec in files:
		stored = store_bytes(
			spec["content"].encode("utf-8"),
			root,
			("Test Data", "Computer Systems", "Lecture 01"),
			spec["filename"],
		)
		file_doc = _get_or_insert(
			"Academic File",
			{
				"canonical_course": course.name,
				"sha256": stored["sha256"],
				"original_filename": stored["original_filename"],
			},
			{
				"vault_relative_path": stored["vault_relative_path"],
				"byte_size": stored["byte_size"],
				"content_type": stored["content_type"],
				"data_origin": "Test data",
				"source_course_mapping": mappings[spec["source"]].name,
				"source_system": spec["source"],
				"external_object_id": spec["external_object_id"],
			},
		)
		resource = _get_or_insert(
			"Academic Resource",
			{"canonical_course": course.name, "title": spec["title"], "data_origin": "Test data"},
			{
				"course_section": section.name,
				"resource_type": spec["resource_type"],
				"source_course_mapping": mappings[spec["source"]].name,
				"source_system": spec["source"],
				"external_object_id": spec["external_object_id"],
				"source_title": spec["title"],
				"sync_state": "Local only",
				"description": TEST_NOTE,
				"source_metadata": _source_metadata(spec["source"], spec["external_object_id"]),
			},
		)
		if not file_doc.academic_resource:
			file_doc.academic_resource = resource.name
			file_doc.save(ignore_permissions=True)

	_get_or_insert(
		"Academic Resource",
		{"canonical_course": course.name, "title": "Attendance snapshot (synthetic)", "data_origin": "Test data"},
		{
			"resource_type": "Attendance Snapshot",
			"source_course_mapping": mappings["APSpace"].name,
			"source_system": "APSpace",
			"external_object_id": "TEST-APSPACE-ATTENDANCE-01",
			"source_title": "Attendance snapshot (synthetic)",
			"sync_state": "Local only",
			"description": TEST_NOTE,
			"content_text": "Session 1: present (synthetic example only).",
			"source_metadata": _source_metadata("APSpace", "TEST-APSPACE-ATTENDANCE-01"),
		},
	)
	_get_or_insert(
		"Academic Resource",
		{"canonical_course": course.name, "title": "My revision note", "data_origin": "Personal"},
		{
			"resource_type": "Personal Note",
			"content_text": "Personal test note: review the difference between processes and threads.",
			"description": "Personal information; not imported from an external service.",
		},
	)
	_get_or_insert(
		"Academic Assignment",
		{"canonical_course": course.name, "title": "Assignment 01 (synthetic)", "data_origin": "Test data"},
		{
			"due_at": "2026-10-07 23:59:00",
			"due_timezone": "Asia/Riyadh",
			"status": "Open",
			"source_course_mapping": mappings["Moodle"].name,
			"source_system": "Moodle",
			"external_object_id": "TEST-MOODLE-ASSIGNMENT-01",
			"source_title": "Assignment 01 (synthetic)",
			"description": TEST_NOTE,
			"source_metadata": _source_metadata("Moodle", "TEST-MOODLE-ASSIGNMENT-01"),
		},
	)
	frappe.db.commit()
	return course.name
