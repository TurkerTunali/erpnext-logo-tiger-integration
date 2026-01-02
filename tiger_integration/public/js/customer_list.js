frappe.listview_settings["Customer"] = {
	onload: function (listview) {
		console.log("Started");
		var method = "tiger_integration.api.logo_sync.bulk_export_to_logo";

		listview.page.add_action_item(__("Logo Export"), function () {
			listview.call_for_selected_items(method, { doctype: "Customer" });
		});
	},
};