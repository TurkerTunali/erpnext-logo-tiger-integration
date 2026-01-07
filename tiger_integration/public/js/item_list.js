frappe.listview_settings["Item"] = {
	onload: function (listview) {
		var method = "tiger_integration.api.logo_sync.bulk_export_to_logo";

		listview.page.add_action_item(__("Logo Export"), function () {
			// Standard call
			listview.call_for_selected_items(method, { doctype: "Item" });
		});

		// 1. Listen for Progress Bar
		frappe.realtime.on("logo_progress", function (data) {
			frappe.show_progress(__("Exporting to Logo"), data.current, data.total, "Please wait...");
		});

		// 2. Listen for Completion Report
		frappe.realtime.on("logo_done", function (data) {
			frappe.hide_progress();

			let msg = `<b>${__('Export Complete')}</b><br>`;
			msg += `${__('Success')}: ${data.success}<br>`;
			msg += `${__('Failed')}: ${data.failed}`;

			if (data.errors && data.errors.length > 0) {
				// Show first 10 errors max to prevent popup flooding
				msg += "<hr>" + data.errors.slice(0, 10).join("<br>");
				if (data.errors.length > 10) msg += "<br>...and more errors.";
			}

			frappe.msgprint({
				title: __("Logo Export Result"),
				message: msg,
				indicator: data.failed === 0 ? 'green' : 'orange',
				wide: true
			});
		});
	},
};
