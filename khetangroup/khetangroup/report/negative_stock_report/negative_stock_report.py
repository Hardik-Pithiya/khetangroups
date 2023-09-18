import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns(filters)
    bin_entries = get_bin_entries(filters)

    data = []
    for sl_name in bin_entries:
        data.append(sl_name)
    return columns, data

def get_columns(filters):
    columns = [
     
        {
            "label": _("Item Name"),
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 200,
        },
        {
            "label": _("Warehouse"),
            "fieldname": "warehouse",
            "fieldtype": "Link",
            "options": "Warehouse",
            "width": 150,
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
            }
        ]
    )

    return columns


def get_bin_entries(filters):
    from_date = filters.get('from_date')
    to_date = filters.get('to_date')
    item_code = filters.get('item_code')
    item_group = filters.get('item_group')
    data_query = f"""
    			SELECT se.item_code,se.warehouse,SUM(se.actual_qty) AS "qty" FROM `tabBin` se , `tabItem` sei WHERE se.item_code = sei.item_code 
       AND 
       sei.company_unit = "Unit 1"
       AND
       sei.disabled = 0
       AND se.actual_qty < 0 AND
       se.creation  BETWEEN '{from_date}' AND '{to_date}'"""
    if item_code:
        data_query += f"AND se.item_code = '{item_code}'"
    if item_group:
        data_query += f"AND sei.item_group = '{item_group}'"
    data_query += "GROUP BY se.item_code,se.warehouse"
    
    return frappe.db.sql(data_query, as_dict = True)


def get_conditions(filters):
    conditions = {}

    for key, value in filters.items():
        if filters.get(key):
            conditions[key] = value
    return conditions
