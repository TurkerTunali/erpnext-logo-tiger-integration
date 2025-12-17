# Copyright (c) 2025, Logedosoft Business Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LOGOObjectServiceSettings(Document):
	@frappe.whitelist()
	def test_connection(self):
		import requests
		from bs4 import BeautifulSoup
		import html
	
		dctResult = frappe._dict({
			"op_result": True,
			"op_message": "",
			"raw_response": ""
		})

		# Ensure user can read this doc
		self.check_permission("read")

		frappe.log_error("K1", self.lobject_service_client_secret)

		try:
			soap_body = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
				  xmlns:tem="http://tempuri.org/"
				  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <soapenv:Header/>
  <soapenv:Body>
	<tem:getInfo>
	  <tem:resultXML xsi:nil="true" />
	  <tem:securityCode>{self.lobject_service_client_secret}</tem:securityCode>
	</tem:getInfo>
  </soapenv:Body>
</soapenv:Envelope>"""
			
			headers = {
				"Content-Type": "text/xml;charset=UTF-8",
				"Accept-Encoding": "gzip,deflate",
				"SOAPAction": '"http://tempuri.org/ISvc/getInfo"'
			}

			response = requests.post(
				url=self.lobject_service_address,
				data=soap_body,
				headers=headers,
				timeout=10
			)

			frappe.log_error("LOB0", frappe.as_json(response))

			if response.status_code != 200:
				dctResult.op_result = False
				dctResult.op_message = f"HTTP Error {response.status_code}: {response.reason}"
			else:
				dctResult.raw_response = response.text
				soup = BeautifulSoup(response.content, 'xml')
				result_xml = soup.find('resultXML')

				if not result_xml or not result_xml.text:
					dctResult.op_message = "Connected but no data returned!"
				else:
					inner_xml = html.unescape(result_xml.text)
					inner_soup = BeautifulSoup(inner_xml, 'xml')

					version = inner_soup.find('LogoObjectsVersion').text
					service_ver = inner_soup.find('ServiceVersion').text
					firm_nr = inner_soup.find('FirmNr').text

					dctResult.op_result = True
					dctResult.op_message = f"Connected!<br><br>LOGO: {version}<br>Service: {service_ver}<br>Firm: {firm_nr}"

		except Exception as e:
			dctResult.op_result = False
			dctResult.op_message = f"LOGO Object Service Connection failed: {e}"

		return dctResult