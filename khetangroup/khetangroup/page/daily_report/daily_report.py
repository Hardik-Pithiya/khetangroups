import frappe

@frappe.whitelist()
def get_purchase_orders(start_date, end_date):
    return frappe.db.sql("""
        SELECT name, supplier, supplier_name, transaction_date, schedule_date, company, buying_price_list, price_list_currency, total qty, total
        FROM `tabPurchase Order`
        WHERE transaction_date BETWEEN %s AND %s
    """, (start_date, end_date), as_dict=True)

@frappe.whitelist()
def get_sales_orders(start_date, end_date):
    return frappe.db.sql("""
        SELECT name, customer, customer_name, transaction_date, delivery_date, company, currency, selling_price_list, total qty, total
        FROM `tabSales Order`
        WHERE transaction_date BETWEEN %s AND %s
    """, (start_date, end_date), as_dict=True)


@frappe.whitelist()
def get_stock_entry(start_date, end_date):
    return frappe.db.sql("""
        SELECT name, posting_date, posting_time, stock_entry_type, company, shift_type, from_warehouse, to_warehouse, total_qty, total_outgoing_value, total_incoming_value
        FROM `tabStock Entry`
        WHERE posting_date BETWEEN %s AND %s
    """, (start_date, end_date), as_dict=True)
    
@frappe.whitelist()
def get_card_attendance(start_date, end_date):
    return frappe.db.sql("""
        SELECT employee, employee_name, status, working_hours, attendance_date, company, department, shift, in_time, out_time
        FROM `tabAttendance`
        WHERE attendance_date BETWEEN %s AND %s
    """, (start_date, end_date), as_dict=True)

