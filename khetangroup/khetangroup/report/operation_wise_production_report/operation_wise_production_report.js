// Copyright (c) 2023, khetangroup@gmail.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Operation Wise Production Report"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname":"operation",
			"label": __("Operation"),
			
			"fieldtype":"Link",
			"options":"Operation",
			"reqd":0
		},
		{
			"fieldname":"item_code",
			"label":__("Item Name"),
			"fieldtype":"Link",
			"options":"Item",
			"reqd":0
		}
		
	],
	"formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.fieldname == "out_qty" && data && data.out_qty > 0) {
			value = "<span style='color:red'>" + value + "</span>";
		}
		else if (column.fieldname == "in_qty" && data && data.in_qty > 0) {
			value = "<span style='color:green'>" + value + "</span>";
		}

		return value;
	},
};
