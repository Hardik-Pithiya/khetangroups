# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns(filters)
	sl_name_entries = get_stock_ledger_name_entries(filters)
	sl_entries = get_stock_ledger_entries(filters)
	slm_entries = get_stock_manufacturing_entries(filters)
	scrap_entries = get_stock_scrap_entries(filters)
	reject_entries = get_stock_reject_entries(filters)
	short_entries = get_short_reject_entries(filters)
	straightner_entries = get_stock_straightner_entries(filters)
	data = []
	for sl_name in sl_name_entries:
		
		for slm in slm_entries:
			if sl_name.name == slm.name:

				slm.update({"out_qty": slm.qty})
				data.append(slm)
		for sle in sl_entries:
			if sl_name.name == sle.name:
				sle.update({"in_qty": sle.qty})
				data.append(sle)
	
		for scrap in scrap_entries:
			if sl_name.name == scrap.name:
				scrap.update({"scrap_qty":scrap.qty})
				data.append(scrap)
		for reject in reject_entries:
			if sl_name.name == reject.name:
				reject.update({"reject_qty":reject.qty})
				data.append(reject)
		for short in short_entries:
			if sl_name.name == short.name:
				short.update({"short_qty":short.qty})
				data.append(short)
		for straightner in straightner_entries:
			if sl_name.name == straightner.name:
				straightner.update({"straightner_qty":straightner.qty})
				data.append(straightner)
	return columns, data

	

def get_columns(filters):
	columns = [
		{"label": _("Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 150},
		{
			"label": _("Shift"),
			"fieldname": "shift_type",
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"label": _("Manufacturing Type"),
			"fieldname": "manufacturing_type",
			"fieldtype": "Data",
			"width": 150,
		},
		{
			"label": _("Operation Name"),
			"fieldname": "operation",
			"fieldtype": "Link",
			"options":"Operation",
			"width": 150,
		},
		{
			"label": _("Machine Name"),
			"fieldname": "machine",
			"fieldtype": "Link",
			"options":"Workstation",
			"width": 150,
		},
		{
			"label": _("Supervisor Name"),
			"fieldname": "supervisor_name",
			"fieldtype": "Link",
			"options":"Employee",
			"width": 150,
		},
			{
			"label": _("Senior Operator Name"),
			"fieldname": "senior_operator_name",
			"fieldtype": "Link",
			"options":"Employee",
			"width": 150,
		},
			{
			"label": _("Operator Name"),
			"fieldname": "operator_name",
			"fieldtype": "Link",
			"options":"Employee",
			"width": 150,
		},
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
				"label": _("Finish Qty"),
				"fieldname": "in_qty",
				"fieldtype": "Float",
				"width": 120,
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
				"label": _("Scrap Qty"),
				"fieldname": "scrap_qty",
				"fieldtype": "Float",
				"width": 120,
				"convertible": "qty",
			},
			{
				"label": _("Reject Qty"),
				"fieldname": "reject_qty",
				"fieldtype": "Float",
				"width": 120,
				"convertible": "qty",
			},
			{
				"label": _("Short Qty"),
				"fieldname": "short_qty",
				"fieldtype": "Float",
				"width": 100,
				"convertible": "qty",
			},
			{
				"label": _("Straightner Qty"),
				"fieldname": "straightner_qty",
				"fieldtype": "Float",
				"width": 120,
				"convertible": "qty",
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

def get_stock_ledger_name_entries(filters):
	sle = frappe.qb.DocType("Stock Entry")
	
	query = (
		frappe.qb.from_(sle)
		
		.select(
			
				sle.name,
			
		)
		.where(
			(sle.stock_entry_type == "Manufacturing Unit-2")
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
			sle.manufacturing_type,
			sle.operation,
			sle.supervisor_name,
			sle.senior_operator_name,	
			sed.item_name,
			sle.posting_date,
			sed.qty,
			sle.stock_entry_type,
			sle.machine,
			sle.operator_name,
			sle.name,	
			sle.shift_type,
			
		)
		.where(
			(sle.stock_entry_type == "Manufacturing Unit-2")
			&(sed.s_warehouse != "")
				& (sle.docstatus == 1)
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
			(sle.stock_entry_type == "Manufacturing Unit-2")
			& (sle.docstatus == 1)
			&(sed.is_finished__item == 1)
			& (sle.posting_date[filters.from_date : filters.to_date])
		)
		
	)

	return query.run(as_dict=True)



	
def get_stock_scrap_entries(filters):
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
			(sle.stock_entry_type == "Manufacturing Unit-2")
			& (sle.docstatus == 1)
			&(sed.is_scrap_item == 1)
			& (sle.posting_date[filters.from_date : filters.to_date])
		)
		
	)

	return query.run(as_dict=True)

def get_stock_reject_entries(filters):
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
			(sle.stock_entry_type == "Manufacturing Unit-2")
			& (sle.docstatus == 1)
			&(sed.rejected_item == 1)
			& (sle.posting_date[filters.from_date : filters.to_date])
		)
		
	)

	return query.run(as_dict=True)

def get_short_reject_entries(filters):
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
			(sle.stock_entry_type == "Manufacturing Unit-2")
			& (sle.docstatus == 1)
			&(sed.short_length == 1)
			& (sle.posting_date[filters.from_date : filters.to_date])
		)
		
	)

	return query.run(as_dict=True)

def get_stock_straightner_entries(filters):
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
			(sle.stock_entry_type == "Manufacturing Unit-2")
			& (sle.docstatus == 1)
			&(sed.straightner == 1)
			& (sle.posting_date[filters.from_date : filters.to_date])
		)
		
	)

	return query.run(as_dict=True)