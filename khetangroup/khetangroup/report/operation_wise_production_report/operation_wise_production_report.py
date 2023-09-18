import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns(filters)
    sl_entries = get_stock_ledger_entries(filters)

    data = []
    for sl_name in sl_entries:
      
        
        data.append(sl_name)
    return columns, data

def get_columns(filters):
    columns = [
        {"label": _("Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 200},
        {
            "label": _("Item Name"),
            "fieldname": "item_name",
            "fieldtype": "Data",
            "options": "Item",
            "width": 300,
        },
    ]

    columns.extend(
        [
            {
                "label": _("Qty"),
                "fieldname": "qty",
                "fieldtype": "Float",
                "width": 180,
                "convertible": "qty",
            },
          
            {
                "label": _("Operation Name"),
                "fieldname": "operation",
                "fieldtype": "Link",
                "options": "Operation",
                "width": 200,
            },
        ]
    )

    return columns

def get_stock_ledger_entries(filters):
    from_date = filters.get('from_date')
    to_date = filters.get('to_date')
    item_code = filters.get('item_code')
    operation = filters.get('operation')

    query = f"""SELECT se.posting_date, se.operation, sed.item_name, SUM(sed.qty) AS "qty"
                FROM `tabStock Entry` se 
                JOIN `tabStock Entry Detail` sed ON se.name = sed.parent
                WHERE se.stock_entry_type = "Manufacturing"
                AND sed.is_finished_item = 1
                AND se.posting_date BETWEEN '{from_date}' AND '{to_date}'"""
	
    if item_code:
        query += f" AND sed.item_code = '{item_code}'"
        
    if operation:
        query += f" AND se.operation = '{operation}'"

    query += " GROUP BY sed.item_code, se.operation"

    return frappe.db.sql(query, as_dict=True)



def get_conditions(filters):
    conditions = {}

    for key, value in filters.items():
        if filters.get(key):
            conditions[key] = value
    return conditions
