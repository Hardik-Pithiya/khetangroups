# Copyright (c) 2023, khetangroup and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from khetangroup.khetangroup.qr_demo import get_qr_code
class QrCode(Document):
	def validate(self):
		self.qr_data = get_qr_code({"Product Name":self.item_code ,"MRP":self.mrp,"Manufacturing Date":self.manufacturing_date ,"Size":self.size,"Color":self.color})
