import frappe


def ensure_unique_constraints():
	frappe.db.add_unique(
		"External Course Mapping",
		["source_system", "external_course_id"],
		"uniq_studies_external_course",
	)
	frappe.db.add_unique(
		"Academic File",
		["canonical_course", "sha256", "original_filename"],
		"uniq_studies_course_file",
	)
