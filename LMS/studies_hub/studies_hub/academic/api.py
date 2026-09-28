import frappe
from frappe import _


def _require_login():
	if frappe.session.user == "Guest":
		frappe.throw(_("Log in to view your academic workspace."), frappe.PermissionError)


@frappe.whitelist()
def get_course_view(course_name=None):
	_require_login()
	courses = frappe.get_list(
		"Canonical Course",
		filters={"name": course_name} if course_name else {"status": "Active"},
		fields=["name", "title", "preferred_short_title", "institution", "program", "academic_year", "term", "status", "data_origin", "description"],
		order_by="title asc",
	)
	if course_name and not courses:
		frappe.throw(_("Course not found."), frappe.DoesNotExistError)
	for course in courses:
		frappe.get_doc("Canonical Course", course.name).check_permission("read")
		course["mappings"] = frappe.get_list(
			"External Course Mapping",
			filters={"canonical_course": course.name},
			fields=["source_system", "external_course_id", "external_code", "external_title", "sync_state", "last_seen_at", "provenance_note"],
			order_by="source_system asc",
		)
		course["sections"] = frappe.get_list(
			"Course Section",
			filters={"canonical_course": course.name},
			fields=["name", "title", "section_type", "position", "data_origin"],
			order_by="position asc, title asc",
		)
		resources = frappe.get_list(
			"Academic Resource",
			filters={"canonical_course": course.name},
			fields=["name", "course_section", "title", "resource_type", "data_origin", "source_system", "source_title", "source_url", "sync_state", "description", "content_text"],
			order_by="title asc",
		)
		for resource in resources:
			resource["files"] = frappe.get_list(
				"Academic File",
				filters={"academic_resource": resource.name},
				fields=["name", "original_filename", "sha256", "byte_size", "data_origin"],
			)
		course["resources"] = resources
		course["assignments"] = frappe.get_list(
			"Academic Assignment",
			filters={"canonical_course": course.name},
			fields=["title", "due_at", "due_timezone", "status", "data_origin", "source_system", "source_title", "description"],
			order_by="due_at asc",
		)
	return {"courses": courses}
