
	// =================================================Getting Purchase order Data============================================================
	function getPurchaseOrders(startDate, endDate) {
		frappe.call({
			method: 'khetangroup.khetangroup.page.daily_report.daily_report.get_purchase_orders',
			args: {
				start_date: startDate,
				end_date: endDate
			},
			callback: function(data) {
				var rows = '';
				$.each(data.message, function(i, d) {
					rows += '<tr><td>' + (d.name ? d.name : '') + '</td><td>' + (d.supplier ? d.supplier : '') + '</td><td>' + (d.supplier_name ? d.supplier_name : '') + '</td><td>' + (d.transaction_date ? d.transaction_date : '') + '</td><td>' + (d.shedule_date ? d.shedule_date : '') + '</td><td>' + (d.company ? d.company : '') + '</td><td>' + (d.buying_price_list ? d.buying_price_list : '') + '</td><td>' + (d.price_list_currency ? d.price_list_currency : '') + '</td><td>' + (d.total_qty ? d.total_qty : '') + '</td><td>' + (d.total ? d.total : '') + '</td></tr>';
				});
				$('#po-table tbody').html(rows);
			}
		});
	}
	
	// =================================================Getting Sales Order Data===============================================================
	function getSalesOrders(startDate, endDate) {
		frappe.call({
			method: 'khetangroup.khetangroup.page.daily_report.daily_report.get_sales_orders',
			args: {
				start_date: startDate,
				end_date: endDate
			},
			callback: function(data) {None
				var rows = '';
				$.each(data.message, function(i, d) {
					rows += '<tr><td>' + (d.name ? d.name : '') + '</td><td>' + (d.customer ? d.customer : '') + '</td><td>' + (d.customer_name ? d.customer_name : '') + '</td><td>' + (d.transaction_date ? d.transaction_date : '') + '</td><td>' + (d.delivery_date ? d.delivery_date : '') + '</td><td>' + (d.company ? d.company : '') + '</td><td>' + (d.currency ? d.currency : '') + '</td><td>' + (d.selling_price_list ? d.selling_price_list : '') + '</td><td>' + (d.total_qty ? d.total_qty : '') + '</td><td>' + (d.total ? d.total : '') + '</td></tr>';
	
				});
				$('#so-table tbody').html(rows);
			}
		});
	}
	// ==================================================Getting Card Attendance details========================================================
	
	function getCarddAttendance(startDate, endDate) {
		frappe.call({
			method: 'khetangroup.khetangroup.page.daily_report.daily_report.get_card_attendance',
			args: {
				start_date: startDate,
				end_date: endDate
			},
			callback: function(data) {
				var rows = '';
				$.each(data.message, function(i, d) {
					rows += '<tr><td>' + (d.employee ? d.employee : '') + '</td><td>' + (d.employee_name ? d.employee_name : '') + '</td><td>' + (d.status ? d.status : '') + '</td><td>' + (d.working_hours ? d.working_hours : '') + '</td><td>' + (d.attendance_date ? d.attendance_date : '') + '</td><td>' + (d.company ? d.company : '') + '</td><td>' + (d.department ? d.department : '') + '</td><td>' + (d.shift ? d.shift : '') + '</td><td>' + (d.in_time ? d.in_time : '') + '</td><td>' + (d.out_time ? d.out_time : '') + '</td></tr>';
	
				});
				$('#ca-table tbody').html(rows);
			}
		});
	}
	
	
	
	// ===================================================Getting stock entry details============================================================
	
	function getStockEntry(startDate, endDate) {
		frappe.call({
			method: 'khetangroup.khetangroup.page.daily_report.daily_report.get_stock_entry',
			args: {
				start_date: startDate,
				end_date: endDate
			},
			callback: function(data) {
				var rows = '';
				$.each(data.message, function(i, d) {
					rows += '<tr><td>' + (d.name ? d.name : '') + '</td><td>' + (d.posting_date ? d.posting_date : '') + '</td><td>' + (d.posting_time ? d.posting_time : '') + '</td><td>' + (d.stock_entry_type ? d.stock_entry_type : '') + '</td><td>' + (d.company ? d.company : '') + '</td><td>' + (d.shift_type ? d.shift_type : '') + '</td><td>' + (d.from_warehouse ? d.from_warehouse : '') + '</td><td>' + (d.to_warehouse ? d.to_warehouse : '') + '</td><td>' + (d.total_qty ? d.total_qty : '') + '</td><td>' + (d.total_outgoing_value ? d.total_outgoing_value : '') + '</td></tr>';
	
				});
				$('#st-table tbody').html(rows);
			}
		});
	}
	
	// =======================================================Frappe Page declaration============================================================
	
	frappe.pages['daily-report'].on_page_load = function(wrapper) {
		var page = frappe.ui.make_app_page({
			parent: wrapper,
			title: 'Report',
			single_column: true
		});
		
	// ==========================================================filter html code================================================================
		var filters = $('<div class="form-group row mainNone-row">\
			<div class=" col ">\
			<div class="row">\
			<div class="col from-col">\
						<label  class="control-label col text-center" id="from-date">From Date :</label>\
					</div>\
					<div class="col">\
						<input type="date"  class="form-control"  id="start-date">\
						</div>\
						</div>\
					</div>\
					<div class=" col ">\
					<div class="row">\
					<div class="col to-col" >\
						<label class="control-label col" id="to-date">To Date :</label>\
					</div>\
					<div class="col">\
						<input type="date"  class="form-control " id="end-date">\
						</div>\
				</div>\
				</div>\
		</div>\
		');
		
		
	// =======================================================Purchase Table =====================================================================
	
	var po = $('<h3 class="mt-5 text-center ">Purchase</h3>')
	
	var po_table = $('<table class="table table-bordered" id="po-table">\
			<thead>\
			<tr>\
			<th>Name</th>\
			<th>Supplier</th>\
			<th>Supplier Name</th>\
			<th>Transaction Date</th>\
			<th>Schedule Date</th>\
			<th>Company</th>\
			<th>Buying Price List</th>\
			<th>Price List Currency</th>\
			<th>Total QTY</th>\
					<th>Total</th>\
				</tr>\
			</thead>\
			<tbody>\
			</tbody>\
		</table>');
	
		
	// ================================================================Sales Table==============================================================
		
		var so = $('<h3 class="mt-5 text-center">Sales</h3>')
		var so_table = $('<table class="table table-bordered" id="so-table">\
	<thead>\
	<tr>\
	<th>Name</th>\
	<th>Customer</th>\
	<th>Customer Name</th>\
	<th>Transaction Date</th>\
	<th>Delivery Date</th>\
	<th>Company</th>\
	<th>Currency</th>\
	<th> Selling Price List </th>\
	<th>Total QTY</th>\
	<th>Total</th>\
	</tr>\
	</thead>\
	<tbody>\
	</tbody>\
	</table>'
	);
	// ================================================================Card Attendance ========================================================
	
	
	var ca = $('<h3 class="mt-5 text-center ">HR</h3>')
	
	var ca_table = $('<table class="table table-bordered" id="ca-table">\
			<thead>\
			<tr>\
			<th>Employee</th>\
			<th>Employee Name</th>\
			<th>Status</th>\
			<th>Working Hours</th>\
			<th>Attendance Date</th>\
			<th>Company</th>\
			<th>Department</th>\
			<th>Shift</th>\
			<th>in_time</th>\
			<th>out_time</th>\
				</tr>\
			</thead>\
			<tbody>\
			</tbody>\
		</table>');
	
	// ===================================================Stock Entry Table===================================================================
	
	var stock_entry = $('<h3 class="mt-5 text-center">Stock Entry</h3>')
	var st_table = $('<table class="table table-bordered" id="st-table">\
	<thead>\
			<tr>\
					<th>Name</th>\
					<th>Posting Date</th>\
					<th>Posting Time</th>\
					<th>Stock Entry Type</th>\
					<th>Company</th>\
					<th>Shift Type</th>\
					<th>From Warehouse</th>\
					<th> To Warehouse </th>\
					<th>Total QTY</th>\
					<th>Total Outgoing Value</th>\
					</tr>\
			</thead>\
			<tbody>\
			</tbody>\
			</table>'
			);
	
	// ===================================================Adding tables to page================================================================
			
			
			page.main.append(filters, po, po_table, so, so_table,ca, ca_table, stock_entry, st_table);
			
	//======================================================= Filtering Dates==================================================================
		
		// Update data when date inputs change
		$('#start-date, #end-date').on('change', function() {
				var startDate = $('#start-date').val();
				var endDate = $('#end-date').val();
				getPurchaseOrders(startDate, endDate);
				getSalesOrders(startDate, endDate);
				getStockEntry(startDate, endDate);
				getCarddAttendance(startDate,endDate);
			});
			
			wrapper.page.set_primary_action('Print', function() {
	
				
				
				
				window.print()
				
				
			});
	
	
			wrapper.page.set_primary_action('Print', function() {
				var style = document.createElement('style');
				style.textContent = '@media print { .page-head{ display:none;} .page-body{margin-top:3rem}}';
				document.head.appendChild(style);
				window.print();
			  });
			
	
		};
