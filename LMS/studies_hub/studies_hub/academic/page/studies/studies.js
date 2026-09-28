frappe.pages["studies"].on_page_load = function (wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __("Studies Hub"),
		single_column: true,
	});
	page.main.addClass("studies-hub-page");
	wrapper.studiesHubPage = page;

	const esc = (value) => String(value ?? "").replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[char]);
	const badge = (value) => `<span class="sh-badge">${esc(value || "Local only")}</span>`;

	page.load_courses = async function () {
		page.main.html('<div class="sh-loading">Loading local course data…</div>');
		const route = frappe.get_route();
		const courseName = route.length > 1 ? route[1] : null;
		try {
			const response = await frappe.call({
				method: "studies_hub.academic.api.get_course_view",
				args: { course_name: courseName },
			});
			const courses = response.message.courses || [];
			if (!courses.length) {
				page.main.html('<div class="sh-empty">No courses yet. Add a Canonical Course from the Academic module.</div>');
				return;
			}
			if (!courseName) {
				page.main.html(`<div class="sh-course-grid">${courses.map((course) => `
					<button class="sh-course-card" data-course="${esc(course.name)}">
						<span class="sh-kicker">${esc(course.institution || "Personal study")}</span>
						<strong>${esc(course.title)}</strong>
						<span>${esc([course.academic_year, course.term].filter(Boolean).join(" · "))}</span>
						${badge(course.data_origin)}
					</button>`).join("")}</div>`);
				page.main.find(".sh-course-card").on("click", function () {
					frappe.set_route("studies", $(this).data("course"));
				});
				return;
			}

			const course = courses[0];
			const sourceRows = course.mappings.map((mapping) => `
				<div class="sh-source-row">
					<div><strong>${esc(mapping.source_system)}</strong><span>${esc(mapping.external_title || "")}</span></div>
					<div class="sh-source-meta"><code>${esc(mapping.external_course_id)}</code>${mapping.external_code ? `<code>${esc(mapping.external_code)}</code>` : ""}${badge(mapping.sync_state)}</div>
					<p>${esc(mapping.provenance_note || "Source identity stored locally")}</p>
				</div>`).join("");
			const materials = course.resources.filter((item) => item.data_origin !== "Personal");
			const personal = course.resources.filter((item) => item.data_origin === "Personal");
			const renderResource = (item) => `
				<article class="sh-resource">
					<div class="sh-resource-head"><strong>${esc(item.title)}</strong>${badge(item.data_origin)}</div>
					<div class="sh-muted">${esc(item.resource_type)}${item.source_system ? ` · ${esc(item.source_system)}` : ""}${item.course_section ? ` · ${esc(course.sections.find((section) => section.name === item.course_section)?.title || "")}` : ""}</div>
					${item.description ? `<p>${esc(item.description)}</p>` : ""}
					${item.content_text ? `<pre>${esc(item.content_text)}</pre>` : ""}
					${item.files.map((file) => `<a class="sh-file" href="/api/method/studies_hub.vault.api.open_local_file?file_id=${encodeURIComponent(file.name)}">Open local file: ${esc(file.original_filename)} <small>${esc(file.sha256.slice(0, 12))} · ${esc(file.byte_size)} bytes</small></a>`).join("")}
				</article>`;
			const assignmentRows = course.assignments.map((assignment) => `
				<div class="sh-assignment"><div><strong>${esc(assignment.title)}</strong><p>${esc(assignment.description || "")}</p></div><div class="sh-due">${esc(assignment.due_at || "No due date")}<small>${esc(assignment.due_timezone)}</small>${badge(assignment.data_origin)}</div></div>`).join("");
			page.main.html(`
				<button class="sh-back">← ${__("All courses")}</button>
				<div class="sh-test-banner">Synthetic demonstration · not official university information · external services were never contacted</div>
				<header class="sh-course-header"><div><span class="sh-kicker">${esc(course.institution || "Local study")}</span><h1>${esc(course.title)}</h1><p>${esc(course.description || "")}</p></div><div class="sh-term">${esc([course.academic_year, course.term].filter(Boolean).join(" · "))}</div></header>
				<section class="sh-panel"><div class="sh-panel-title"><h2>External course identities</h2><span>One local course · ${course.mappings.length} simulated mappings</span></div><div class="sh-sources">${sourceRows}</div></section>
				<section class="sh-panel"><div class="sh-panel-title"><h2>Course materials</h2><span>Local copies remain available offline</span></div><div class="sh-resource-list">${materials.map(renderResource).join("") || '<p class="sh-muted">No local materials yet.</p>'}</div></section>
				<section class="sh-panel"><div class="sh-panel-title"><h2>Assignments</h2><span>Deadline includes its timezone</span></div><div class="sh-assignment-list">${assignmentRows || '<p class="sh-muted">No assignments yet.</p>'}</div></section>
				<section class="sh-panel sh-personal"><div class="sh-panel-title"><h2>My notes</h2><span>Personal data is separate from source records</span></div><div class="sh-resource-list">${personal.map(renderResource).join("") || '<p class="sh-muted">No personal notes yet.</p>'}</div></section>
			`);
			page.main.find(".sh-back").on("click", () => frappe.set_route("studies"));
		} catch (error) {
			page.main.html(`<div class="sh-error">${esc(error.message || "Could not load local course data.")}</div>`);
		}
	};
	page.load_courses();
};

frappe.pages["studies"].on_page_show = function (wrapper) {
	if (wrapper.studiesHubPage?.load_courses) wrapper.studiesHubPage.load_courses();
};
