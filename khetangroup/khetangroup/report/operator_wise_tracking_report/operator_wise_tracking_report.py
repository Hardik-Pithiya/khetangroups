# Copyright (c) 2023, khetangroup and contributors
# For license information, please see license.txt

# import frappe


import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns(filters)
	sl_entries = get_stock_ledger_entries(filters)
	slm_entries = get_stock_manufacturing_entries(filters)
	data = []
	for sle in sl_entries:
		sle.update({"out_qty": max(sle.qty, 0)})
		data.append(sle)
	
	for slm in slm_entries:
		slm.update({"in_qty": max(slm.qty, 0)})
		data.append(slm)

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
				"label": _("Machine Name"),
				"fieldname": "machine",
				"fieldtype": "Link",
				"width": 120,
				"options":"Workstation",
			},
				{
				"label": _("Operator Name"),
				"fieldname": "operator_name",
				"fieldtype": "Link",
				"width": 120,
				"options":"Employee",
			},

			{
				"label": _("Voucher Type"),
				"fieldname": "stock_entry_type",
				"fieldtype": "Link",
				"options": "Stock Entry Type",
				"width": 150,
			},
			
			
			
			
			
		]
	)

	return columns


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
			
		)
		.where(
			(sle.stock_entry_type == "Material Issue")
			& (sle.docstatus == 1)
			& (sle.posting_date[filters.from_date : filters.to_date])
		)
		
	)

	return query.run(as_dict=True)


def get_stock_manufacturing_entries(filters):
	sle = frappe.qb.DocType("Stock Entry")
	sed = frappe.qb.DocType("Stock Entry Detail")
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
			
		)
		.where(
			(sle.stock_entry_type == "Manufacturing Unit-2")
			& (sed.is_finished_item == 1)
				& (sle.docstatus == 1)
			& (sle.posting_date[filters.from_date : filters.to_date])
		)
		
	)

	return query.run(as_dict=True)