import frappe

def daily():
    frappe.get_doc({
        "doctype": "Scheduler Log",
        "event": "khetangroup.update_stock_entry.update_stock_entry",
        "method": "khetangroup.update_stock_entry.update_stock_entry",
        "status": "Queued",
        "start": frappe.utils.now(),
        "user": "Administrator"
    }).insert(ignore_permissions=True)