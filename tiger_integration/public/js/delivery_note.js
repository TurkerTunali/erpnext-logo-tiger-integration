// Copyright (c) 2025, Logedosoft Business Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on("Delivery Note", {
	refresh(frm) {
		//Create custom button to start Logo Sync
		frm.add_custom_button(__("Logo Export"), function() {
			frappe.call({
				method: "tiger_integration.api.logo_sync.export_to_logo",
				args: {
					doctype: "Delivery Note",
					docname: frm.doc.name
				},
				callback: function(r) {
					console.log(r);
					frappe.msgprint({
						title: __("Logo Operation Result"),
						message: r.message.op_message,
						indicator: r.message.op_result ? "green" : "red"
					});
					if (r.message.op_result == true) {
						frm.reload_doc()
					}
				}
			});
		}, __("Actions"));
	}
});