// Copyright (c) 2025, Logedosoft Business Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on("LOGO SQL Settings", {
	async btn_test_connection(frm) {
		const r = await frm.call("test_connection");
		console.log(r);
		if (r.message.op_result == true) {
			frappe.msgprint(r.message.op_message);
		} else {
			frappe.throw(r.message.op_message);
		}
	}
});