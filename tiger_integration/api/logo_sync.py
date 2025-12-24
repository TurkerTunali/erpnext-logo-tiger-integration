# -*- coding: utf-8 -*-
# LOGEDOSOFT

import frappe, json
from frappe import msgprint, _

from frappe.model.document import Document
from frappe.utils import cint, flt

import requests
from bs4 import BeautifulSoup
import html

def get_logo_xml(doctype, docLObjectServiceSettings):
	#Gets info from LOGO Object Service Settings -> Mappings table
	dctResult = frappe._dict({
		"op_result": False,
		"op_message": "",
		"xml_template": "",
		"parameter_xml": ""
	})

	for xml_template in docLObjectServiceSettings.logo_xml_templates:
		if xml_template.document_type == doctype:
			dctResult.op_result = True
			dctResult.xml_template = xml_template.logo_xml_template
			if xml_template.parameter_xml:
				dctResult.parameter_xml = xml_template.parameter_xml
			elif docLObjectServiceSettings.default_parameter_xml:
				dctResult.parameter_xml = xml_template.parameter_xml
			else:
				dctResult.parameter_xml = """
<Parameters>
  <ReplicMode>0</ReplicMode>
  <CheckParams>1</CheckParams>
  <CheckRight>1</CheckRight>
  <ApplyCampaign>1</ApplyCampaign>
  <ApplyCondition>1</ApplyCondition>
  <FillAccCodes>1</FillAccCodes>
  <FormSeriLotLines>0</FormSeriLotLines>
  <GetStockLinePrice>0</GetStockLinePrice>
  <ExportAllData>1</ExportAllData>
  <Validation>0</Validation>
  <CheckApproveDate>0</CheckApproveDate>
  <Period>01</Period>
</Parameters>
"""
	if dctResult.op_result == False and doctype == "Item":
		dctResult.op_result = True
		dctResult.xml_template = """<soapenv:Envelope 
	xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
	xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
	  <tem:AppendDataObject>
		 <tem:dataType>{{ doc.logo_dataType }}</tem:dataType>
		 <tem:dataReference>0</tem:dataReference>
		 <tem:dataXML>
			<![CDATA[<ITEMS>
  <ITEM DBOP="INS">
	<CARD_TYPE>1</CARD_TYPE>
	<CODE>{{ doc.name }}</CODE>
	<NAME>{{ doc.item_name }}</NAME>
    <GROUP_CODE>{{ doc.item_group }}</GROUP_CODE>
    <PRODUCER_CODE></PRODUCER_CODE>
    <AUXIL_CODE></AUXIL_CODE>
    <AUTH_CODE></AUTH_CODE>
    <USEF_PURCHASING>1</USEF_PURCHASING>
    <USEF_SALES>1</USEF_SALES>
    <USEF_MM>1</USEF_MM>
    <VAT>{{ doc.logo_tax_rate }}</VAT>
    <AUTOINCSL>1</AUTOINCSL>
    <LOTS_DIVISIBLE>1</LOTS_DIVISIBLE>
    <UNITSET_CODE>{{ doc.logo_unitset_code }}</UNITSET_CODE>
    <DIST_LOT_UNITS>1</DIST_LOT_UNITS>
    <COMB_LOT_UNITS>1</COMB_LOT_UNITS>
    <UNITS>
      <UNIT>
        <UNIT_CODE>{{ doc.logo_unit_code }}</UNIT_CODE>
        <USEF_MTRLCLASS>1</USEF_MTRLCLASS>
        <USEF_PURCHCLAS>1</USEF_PURCHCLAS>
        <USEF_SALESCLAS>1</USEF_SALESCLAS>
        <CONV_FACT1>1</CONV_FACT1>
        <CONV_FACT2>1</CONV_FACT2>
      </UNIT>
    </UNITS>
    <MULTI_ADD_TAX>0</MULTI_ADD_TAX>
    <PACKET>0</PACKET>
    <SELVAT>{{ doc.logo_tax_rate }}</SELVAT>
    <RETURNVAT>{{ doc.logo_tax_rate }}</RETURNVAT>
    <SELPRVAT>{{ doc.logo_tax_rate }}</SELPRVAT>
    <RETURNPRVAT>{{ doc.logo_tax_rate }}</RETURNPRVAT>
    <MARKCODE></MARKCODE>
    <AUXIL_CODE2></AUXIL_CODE2>
    <AUXIL_CODE3></AUXIL_CODE3>
    <AUXIL_CODE4>{{ doc.brand or '' }}</AUXIL_CODE4>
    <AUXIL_CODE5>{{ doc.custom_manufacturer or '' }}</AUXIL_CODE5>
    <UPDATECHILDS>1</UPDATECHILDS>
  </ITEM>
</ITEMS>]]>
		 </tem:dataXML>

		 <tem:paramXML>
			<![CDATA[{{ parameterXML }}]]>
		 </tem:paramXML>
		 <tem:FirmNr>1</tem:FirmNr>
		 <tem:securityCode>5edd8e65-0292-4318-98bd-e5dccc21d2d9</tem:securityCode>
	  </tem:AppendDataObject>
   </soapenv:Body>
</soapenv:Envelope>"""
		dctResult.parameter_xml = """
<Parameters>
  <ReplicMode>0</ReplicMode>
  <CheckParams>1</CheckParams>
  <CheckRight>1</CheckRight>
  <ApplyCampaign>1</ApplyCampaign>
  <ApplyCondition>1</ApplyCondition>
  <FillAccCodes>1</FillAccCodes>
  <FormSeriLotLines>0</FormSeriLotLines>
  <GetStockLinePrice>0</GetStockLinePrice>
  <ExportAllData>1</ExportAllData>
  <Validation>0</Validation>
  <CheckApproveDate>0</CheckApproveDate>
  <Period>01</Period>
</Parameters>"""
	if dctResult.op_result == False and doctype == "Customer":
		dctResult.op_result = True
		dctResult.xml_template = """<soapenv:Envelope
	xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
	xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
	  <tem:AppendDataObject>
		 <tem:dataType>{{ doc.logo_dataType }}</tem:dataType>
		 <tem:dataReference>0</tem:dataReference>
		 <tem:dataXML>
			<![CDATA[<?xml version="1.0" encoding="ISO-8859-9"?>
<AR_APS>
  <AR_AP DBOP="INS" >
    <ACCOUNT_TYPE>1</ACCOUNT_TYPE>
    <CODE>{{ doc.name }}</CODE>
    <TITLE>{{ doc.customer_name }}</TITLE>
    <CORRESP_LANG>1</CORRESP_LANG>
    <NOTES>
      <NOTE>
        <INTERNAL_REFERENCE>0</INTERNAL_REFERENCE>
      </NOTE>
    </NOTES>
    <CL_ORD_FREQ>1</CL_ORD_FREQ>
    <INVOICE_PRNT_CNT>1</INVOICE_PRNT_CNT>
    <PARENTCLCODE>{{ doc.logo_parent_code }}</PARENTCLCODE>
	<PERSCOMPANY>{{ doc.personal_company }}</PERSCOMPANY>
    <ORGLOGOID></ORGLOGOID>
	<ADDRESS1>{{ docBillingAddress.address_line1 }}</ADDRESS1>
    <ADDRESS2>{{ docBillingAddress.address_line2 or '' }}</ADDRESS2>
    <DISTRICT_CODE></DISTRICT_CODE>
    <DISTRICT></DISTRICT>
    <TOWN_CODE></TOWN_CODE>
    <TOWN>{{ docBillingAddress.county or '' }}</TOWN>
    <CITY_CODE></CITY_CODE>
    <CITY>{{ docBillingAddress.city or '' }}</CITY>
    <COUNTRY_CODE></COUNTRY_CODE>
    <COUNTRY>{{ docBillingAddress.country or '' }}</COUNTRY>
    <TELEPHONE1></TELEPHONE1>
    <TELEPHONE1_CODE></TELEPHONE1_CODE>
    <TELEPHONE2></TELEPHONE2>
    <TELEPHONE2_CODE></TELEPHONE2_CODE>
    <TAX_ID>{{ doc.tax_id or '' }}</TAX_ID>
    <TAX_OFFICE>{{ doc.custom_tax_office or '' }}</TAX_OFFICE>
    <CONTACT></CONTACT>
    <PAYMENT_CODE>{{ doc.logo_payment_term }}</PAYMENT_CODE>
    <E_MAIL></E_MAIL>
	<AUXIL_CODE>{{ doc.customer_group }}</AUXIL_CODE>
	<AUXIL_CODE5>{{ doc.territory }}</AUXIL_CODE5>
	<CONTACT2></CONTACT2>
    <E_MAIL2></E_MAIL2>
    <PURCHBRWS>1</PURCHBRWS>
    <SALESBRWS>1</SALESBRWS>
    <IMPBRWS>1</IMPBRWS>
    <EXPBRWS>1</EXPBRWS>
    <FINBRWS>1</FINBRWS>
    <COLLATRLRISK_TYPE>1</COLLATRLRISK_TYPE>
    <EBANKCODE>-7</EBANKCODE>
    <RISK_TYPE1>1</RISK_TYPE1>
    <RISK_TYPE2>1</RISK_TYPE2>
    <RISK_TYPE3>1</RISK_TYPE3>
    <PROFILE_ID>2</PROFILE_ID>
    <PROFILEID_DESP>1</PROFILEID_DESP>
    <DISP_PRINT_CNT>1</DISP_PRINT_CNT>
    <ORD_PRINT_CNT>1</ORD_PRINT_CNT>
  </AR_AP>
</AR_APS>]]>
		 </tem:dataXML>

		 <tem:paramXML>
			<![CDATA[{{ parameterXML }}]]>
		 </tem:paramXML>
		 <tem:FirmNr>1</tem:FirmNr>
		 <tem:securityCode>5edd8e65-0292-4318-98bd-e5dccc21d2d9</tem:securityCode>
	  </tem:AppendDataObject>
   </soapenv:Body>
</soapenv:Envelope>"""
		dctResult.parameter_xml = """
<Parameters>
  <ReplicMode>0</ReplicMode>
  <CheckParams>1</CheckParams>
  <CheckRight>1</CheckRight>
  <ApplyCampaign>1</ApplyCampaign>
  <ApplyCondition>1</ApplyCondition>
  <FillAccCodes>1</FillAccCodes>
  <FormSeriLotLines>0</FormSeriLotLines>
  <GetStockLinePrice>0</GetStockLinePrice>
  <ExportAllData>1</ExportAllData>
  <Validation>0</Validation>
  <CheckApproveDate>0</CheckApproveDate>
  <Period>01</Period>
</Parameters>"""

	if dctResult.op_result == False:
		link = frappe.utils.get_link_to_form("LOGO Object Service Settings", _("LOGO Object Service Settings"))
		frappe.throw(_("{0} tipinde {1} için eşleştirme bulunamadı! {2} sayfasında kontrol ediniz").format(doctype, erp_code, link))

	return dctResult

def get_logo_mapping_for(data_type, erp_code, throw_exception = False, docLObjectServiceSettings = None):
	#Gets info from LOGO Object Service Settings -> Mappings table
	dctResult = frappe._dict({
		"op_result": False,
		"op_message": "",
		"op_message_2": ""
	})

	if not docLObjectServiceSettings:
		docLObjectServiceSettings = frappe.get_doc("LOGO Object Service Settings")

	for mapping in docLObjectServiceSettings.mappings:
		if mapping.data_type == data_type:
			if mapping.erp_code == erp_code:
				dctResult.op_message = mapping.logo_code
				dctResult.op_message_2 = mapping.logo_code_2
				dctResult.op_result = True

	if dctResult.op_result == False and throw_exception == True:
		link = frappe.utils.get_link_to_form("LOGO Object Service Settings", _("LOGO Object Service Settings"))
		frappe.throw(_("{0} tipinde {1} için eşleştirme bulunamadı! {2} sayfasında kontrol ediniz").format(data_type, erp_code, link))

	return dctResult

def validate_export_to_logo(doctype, docname, docLObjectServiceSettings):
	doc = frappe.get_doc(doctype, docname)
	doc.check_permission("read")

	if doctype == "Item":
		#Tax must be ok
		if len(doc.taxes) == 0:
			frappe.throw(_("Vergiler tanımlı olmalıdır!"))

		for tax in doc.taxes:
			tax_company = frappe.db.get_value("Item Tax Template", tax.item_tax_template, "company")
			if tax_company == docLObjectServiceSettings.default_company:
				docItemTaxTemplate = frappe.get_doc("Item Tax Template", tax.item_tax_template)
				if len(doc.taxes) == 0:
					frappe.throw("{0} için vergi oranı tanımlı olmalıdır!".format(docItemTaxTemplate.name))

	if doctype == "Customer":
		#Payment Term, default billing address
		if not doc.payment_terms:
			frappe.throw(_("Ödeme Şekli alanı boş bırakılmamalıdır!"))

		#Check billing address
		dctBillingAddress = frappe.get_all("Address",
			filters=[
				["Dynamic Link", "link_doctype", "=", "Customer"],
				["Dynamic Link", "link_name", "=", doc.name],
				["is_primary_address", "=", 1],
				["address_type", "=", "Billing"]
			],
			fields=["name"],
			limit=1
		)
		if not dctBillingAddress:
			frappe.throw(_("Adres tanımlı olmalıdır!"))

@frappe.whitelist(allow_guest=False)
def export_to_logo(doctype, docname, update_logo = False):
	dctResult = frappe._dict({
		"op_result": False,
		"op_message": "",
		"raw_response": "",
		"data_reference": 0,
		"op_status": 0
	})

	doc = frappe.get_doc(doctype, docname)
	doc.check_permission("read")
	docLObjectServiceSettings = frappe.get_doc("LOGO Object Service Settings")
	docLObjectServiceSettings.check_permission("read")

	try:
		dctXMLInfo = get_logo_xml(doctype, docLObjectServiceSettings)
		if dctXMLInfo.op_result == True:
			soap_body = dctXMLInfo.xml_template
			parameterXML = dctXMLInfo.parameter_xml

		if docLObjectServiceSettings.default_parameter_xml:
			parameterXML = docLObjectServiceSettings.default_parameter_xml

		if docLObjectServiceSettings.enable_lobject_service == 0:
			frappe.throw(_("LOGO Object Service aktif değil!"))

		validate_export_to_logo(doctype, docname, docLObjectServiceSettings)

		if doc.doctype == "Item":
			doc.logo_dataType = 0

			dctUnit = get_logo_mapping_for("Unit", doc.stock_uom, throw_exception = True, docLObjectServiceSettings = docLObjectServiceSettings)
			if dctUnit.op_result == True:
				doc.logo_unitset_code = dctUnit.op_message
				doc.logo_unit_code = dctUnit.op_message_2

			#Find tax rate
			for tax in doc.taxes:
				tax_company = frappe.db.get_value("Item Tax Template", tax.item_tax_template, "company")
				if tax_company == docLObjectServiceSettings.default_company:
					docItemTaxTemplate = frappe.get_doc("Item Tax Template", tax.item_tax_template)
					doc.logo_tax_rate = docItemTaxTemplate.taxes[0].tax_rate

			soap_body = frappe.render_template(soap_body, context={'doc': doc, 'docLObjectServiceSettings': docLObjectServiceSettings, 'parameterXML': parameterXML})

		elif doc.doctype == "Customer":
			doc.logo_dataType = 30

			dctCustomerGroup = get_logo_mapping_for("Customer Group", doc.customer_group, throw_exception = True, docLObjectServiceSettings = docLObjectServiceSettings)
			if dctCustomerGroup.op_result == True:
				doc.logo_parent_code = dctCustomerGroup.op_message

			doc.logo_payment_term = ""
			if doc.payment_terms:
				dctPaymentTerm = get_logo_mapping_for("Payment Term Template", doc.payment_terms, throw_exception = True, docLObjectServiceSettings = docLObjectServiceSettings)
				if dctPaymentTerm.op_result == True:
					doc.logo_payment_term = dctPaymentTerm.op_message

			if doc.customer_type == "Individual":
				doc.personal_company = 1
			else:
				doc.personal_company = 0

			dctBillingAddress = frappe.get_all("Address",
				filters=[
					["Dynamic Link", "link_doctype", "=", "Customer"],
					["Dynamic Link", "link_name", "=", doc.name],
					["is_primary_address", "=", 1],
					["address_type", "=", "Billing"]
				],
				fields=["name"],
				limit=1
			)
			if dctBillingAddress:
				docBillingAddress = frappe.get_doc("Address", dctBillingAddress[0].name)
			else:
				frappe.throw(_("Customer has no Billing Address"))

			soap_body = frappe.render_template(soap_body, context={'doc': doc, 'docLObjectServiceSettings': docLObjectServiceSettings, 'docBillingAddress': docBillingAddress, 'parameterXML': parameterXML})
		
		headers = {
			"Content-Type": "text/xml;charset=UTF-8",
			"Accept-Encoding": "gzip,deflate",
			"SOAPAction": "http://tempuri.org/ISvc/AppendDataObject"
		}

		if docLObjectServiceSettings.enable_detailed_log:
			frappe.log_error("LOGO Object Request", f"URL={docLObjectServiceSettings.lobject_service_address}\n\nSOAP Body={soap_body}\n\nSOAP Headers={headers}")

		response = requests.post(
			url=docLObjectServiceSettings.lobject_service_address,
			data=soap_body,#.encode('utf-8'),
			headers=headers,
			timeout=10
		)

		if docLObjectServiceSettings.enable_detailed_log:
			frappe.log_error("LOGO Object Response", f"Status:{response.status_code}\nBody:{response.text}")

		if response.status_code != 200:
			dctResult.op_result = False
			dctResult.op_message = f"HTTP Error {response.status_code}: {response.reason}"
		else:
			dctResult.raw_response = response.text
			soup = BeautifulSoup(response.content, 'xml')
			result_status = soup.find('status')

			if not result_status or not result_status.text:
				dctResult.op_message = "Connected but no status returned!"
			else:
				data_reference = soup.find('dataReference')
				error_string = soup.find('errorString')

				dctResult.data_reference = int(data_reference.text) if data_reference else 0
				dctResult.op_status = int(result_status.text) if result_status else 0
				if dctResult.op_status != 3:
					dctResult.op_result = False
					dctResult.op_message =  (error_string.text if error_string else "") + "(OpStatus=" + str(dctResult.op_status) + ")"
				else:
					dctResult.op_result = True
					dctResult.op_message = data_reference
					doc.add_comment("Comment", text=_("LOGO Export reference no {0}").format(dctResult.data_reference), comment_email=frappe.session.user, comment_by=frappe.session.user)

	except Exception as e:
		dctResult.op_result = False
		dctResult.op_message = str(e) + "\n\n" + frappe.get_traceback()

	return dctResult

def gzip_zip_base64(content):
	import gzip
	import base64
	import sys
	import os
	"""
		 gzip + base64 compression
				 In this way the compressed object relatively short / small when the effect is not obvious, but since then base64 becomes large, but the compression is relatively large when the object will be effective
	:param content:
	:return:
	"""
	bytes_com = gzip.compress(str(content).encode("utf-8"))
	base64_data = base64.b64encode(bytes_com)
	back = str(base64_data.decode())
	return back, sys.getsizeof(back)
	# Gzip file for read and write operations
	# with gzip.open('./log/zip-test.gz', 'wb') as write:
	#     write.write(str(back).encode("utf-8"))

def gzip_unzip_base64(content):
	import gzip
	import base64
	import sys
	import os
	"""
		 base64 + gzip decompression
	:param content:
	:return:
	"""
	base64_data = base64.b64decode(content)
	bytes_decom = gzip.decompress(base64_data)
	str_unzip = bytes_decom.decode()
	return str_unzip, sys.getsizeof(str_unzip)