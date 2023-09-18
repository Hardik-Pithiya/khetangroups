# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns(filters)
	sl_name_entries = get_stock_name_entries(filters)
	sl_entries = get_stock_ledger_entries(filters)
	slm_entries = get_stock_manufacturing_entries(filters)
	data = []
	for sl_name in sl_name_entries:

		for slm in slm_entries:
			if sl_name.name == slm.name:

				slm.update({"out_qty": max(slm.qty, 0)})
				data.append(slm)
		for sle in sl_entries:
			if sl_name.name == sle.name:
				sle.update({"in_qty": max(sle.qty, 0)})
				data.append(sle)
	
	

	return columns, data

	

def get_columns(filters):
	columns = [
		{"label": _("Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 150},
		{
			"label": _("Item Name"),
			"fieldname": "item_name",
			"fieldtype": "Link",
			"options": "Item",
			"width": 150,
		},
		# {"label": _("Item Name"), "fieldname": "item_name", "width": 100},
		
	]

	

	columns.extend(
		[
			{
				"label": _("In Qty"),
				"fieldname": "in_qty",
				"fieldtype": "Float",
				"width": 80,
				"convertible": "qty",
			},
			{
				"label": _("Out Qty"),
				"fieldname": "out_qty",
				"fieldtype": "Float",
				"width": 80,
				"convertible": "qty",
			},
				{
				"label": _("Balance Qty"),
				"fieldname": "balance_qty",
				"fieldtype": "Float",
				"width": 100,
				"convertible": "qty",
			},
			{
				"label": _("Delievry Note No."),
				"fieldname": "delivery_note",
				"fieldtype": "Link",
				"options": "Delivery Note",
				"width": 150,
			},
			
			{
				"label": _("Voucher No."),
				"fieldname": "name",
				"fieldtype": "Link",
				"options": "Stock Entry",
				"width": 180,
			},
			
			
			
			
			
		]
	)

	return columns

def get_stock_name_entries(filters):
	sle = frappe.qb.DocType("Stock Entry")
	
	query = (
		frappe.qb.from_(sle)
	
		.select(
			sle.name,
			
		)
		.where(
			(sle.stock_entry_type == "Subcontracting Received Material")
			
			& (sle.posting_date[filters.from_date : filters.to_date])
		)
		
	)

	return query.run(as_dict=True)


def get_stock_ledger_entries(filters):
	sle = frappe.qb.DocType("Stock Entry")
	sed = frappe.qb.DocType("Stock Entry Detail")
	query = (
		frappe.qb.from_(sle)
		.join(sed)
		.on(sle.name == sed.parent)
		.select(
			sed.item_name,
			sed.machine,
			sed.operator_name,
			sle.posting_date,
			sed.qty,
			sle.stock_entry_type,
			sle.name,
			
		)
		.where(
			(sle.stock_entry_type == "Subcontracting Received Material")
			
			&(sle.docstatus == 1)
			&(sle.delivery_note !="")
			& (sle.posting_date[filters.from_date : filters.to_date])
		)
		
	)

	return query.run(as_dict=True)


def get_stock_manufacturing_entries(filters):
	sle = frappe.qb.DocType("Stock Entry")
	sed = frappe.qb.DocType("Delivery Note Item")
	query = (
		frappe.qb.from_(sle)
		.join(sed)
		.on(sle.name == sed.parent)
		.select(
			sed.item_name,
			sle.posting_date,
			sed.qty,
			sle.stock_entry_type,
			sle.machine,
			sle.operator_name,	
			sle.name,
			sle.delivery_note,
		)
		.where(
			(sle.stock_entry_type == "Subcontracting Received Material")
			
				& (sle.docstatus == 1)
			& (sle.posting_date[filters.from_date : filters.to_date])
		)
		
	)

	return query.run(as_dict=True)