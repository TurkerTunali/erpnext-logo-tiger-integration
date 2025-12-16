# Copyright (c) 2025, Logedosoft Business Solutions and contributors
# For license information, please see license.txt

import frappe
import pymssql
from frappe.model.document import Document

class LOGOSQLSettings(Document):
	@frappe.whitelist()
	def test_connection(self):
		dctResult = frappe._dict({
			"op_result": False,
			"op_message": "",
		})
		# Ensure user can read this doc
		self.check_permission("read")

		host = self.sql_server_address
		#port = 1433#int(self.sql_port or 1433)
		user = self.sql_user_name
		password = self.get_password("sql_user_password")
		database = self.sql_database_name

		try:
			conn = pymssql.connect(
				server=host,
				user=user,
				password=password,
				database=database,
				#port=port,
				login_timeout=5,
				timeout=5,
			)
			cursor = conn.cursor()
			cursor.execute("SELECT GETDATE()")
			data = cursor.fetchone()
			conn.close()
			dctResult.op_result = True
			dctResult.op_message = data[0]

		except Exception as e:
			dctResult.op_result = False
			dctResult.op_message = f"Connection failed: {e}"

		return dctResult