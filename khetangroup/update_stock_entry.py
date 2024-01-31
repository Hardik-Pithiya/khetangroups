import frappe
from frappe.utils import today

@frappe.whitelist()
def update_stock_entry():
    warehouse_name = frappe.db.get_value("Warehouse", filters={'custom_is_party_warehouse': '1'}, fieldname='name')
    quotations = frappe.db.get_all(
    'Quotation',
    filters={
        'valid_till': ("<=",today()),
        'docstatus':1
    },
    fields=['name','total_qty','total_invoice_qty','total_material_return_qty']
)
    
    print("\n\n",quotations,"\n\n")
    for quotation in quotations:
        quotation_item  = frappe.db.get_all("Quotation Item",
        filters={'parent': quotation.name, 'docstatus': 1},
        fields=['item_code', 'qty', 'warehouse','invoice_qty']  # Adjust the fields as needed
        )
        stock_entries = frappe.db.get_all(
        "Stock Entry",
        filters={'quotation_no': quotation.name, 'docstatus': 1,'is_returns':0},
        fields=['name', 'quotation_no']
        )
        
        for stock_entrys in stock_entries:
            total_return_qty = float(quotation.total_material_return_qty)
            total_invoice_qty = float(quotation.total_invoice_qty)
            total_quotation_qty = total_return_qty + total_invoice_qty
            if stock_entrys.quotation_no == quotation.name and total_quotation_qty < quotation.total_qty :
                total_returns_qty = sum([(float(item.qty) - float(item.invoice_qty)) for item in quotation_item])
                stock_entry = frappe.get_doc({
                'doctype': 'Stock Entry',
                'stock_entry_type': 'Material Transfer',
                'quotation_no': quotation.name,
                'is_returns':1,
                'total_qty':total_returns_qty,
                'items': [],
                })
            
                for stock_item in quotation_item:
            
                    if stock_item.invoice_qty != stock_item.qty and quotation.name == stock_entrys.quotation_no:
                        stock_entry.append('items', {
                        'item_code': stock_item.item_code,
                        'qty': (float(stock_item.qty) - float(stock_item.invoice_qty)),
                        't_warehouse': stock_item.warehouse,
                        's_warehouse': warehouse_name
                        
                    
                    # Add other item details as needed
                    })
    # Insert the Stock Entry with all items
                stock_entry.insert()
                stock_entry.submit()
                frappe.db.set_value("Quotation",stock_entrys.quotation_no,'total_material_return_qty',total_returns_qty)
            
