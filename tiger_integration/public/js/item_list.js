frappe.listview_settings["Item"] = {
	onload: function (listview) {
		var method = "tiger_integration.api.logo_sync.bulk_export_to_logo";

		listview.page.add_action_item(__("Logo Export"), function () {
			listview.call_for_selected_items(method, { doctype: "Item" });
		});
	},
};