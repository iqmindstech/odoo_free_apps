# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools import datetime, date


class iqminds_dashboard21(models.Model):
    _name = "iqminds.dashboard"

    sale_order_number = fields.Many2one('sale.order', 'Sale Order No.')
    search_line_ids = fields.Many2many('sale.order', string='Sale Oder')
    invoice_number = fields.Many2one('account.invoice', string='Invoice Number')
    search_line_ids1 = fields.Many2many('account.invoice', string='Invoice')
    customer_name = fields.Many2one('res.partner', 'Customer Name')
    search_line_ids2 = fields.Many2many('res.partner', string='Contact')
    customer_phone = fields.Char('Customer Phone')
    total_sale_order = fields.Integer()
    today_sale_order = fields.Integer()
    today_invoice = fields.Integer()
    total_invoice = fields.Integer()
    total_purchase = fields.Integer()
    today_purchase_order = fields.Integer()
    total_products = fields.Integer()
    total_vendors = fields.Integer()
    total_customers = fields.Integer()
    today_payment_received = fields.Integer()
    total_bill = fields.Integer()
    today_bill_payment = fields.Integer()
    today_bill = fields.Integer()
    total_bill_payment = fields.Integer()
    total_payment_customer = fields.Integer()
    product_available = fields.Integer()
    total_employees = fields.Integer()
    total_expenses = fields.Integer()
    total_receipts = fields.Integer()
    total_delivery = fields.Integer()
    today_receipt = fields.Integer()
    today_delivery = fields.Integer()

    @api.model
    def default_get(self, fields):
        res = super(iqminds_dashboard21, self).default_get(fields)
        current_date = datetime.today().date()
        inv_current_date = date.today()
        val1 = self.get_today_sale_order(current_date)
        val2 = self.get_total_sale_order()
        val3 = self.get_today_invoice(inv_current_date)
        val4 = self.get_total_customers()
        val5 = self.get_total_vendors()
        val6 = self.get_total_invoice()
        val7 = self.get_total_products()
        val8 = self.get_today_purchase(current_date)
        val9 = self.get_total_purchase()
        val10 = self.get_today_payment_received(inv_current_date)
        val11 = self.get_total_bills()
        val12 = self.get_today_bill_payment(inv_current_date)
        val13 = self.get_today_bill(inv_current_date)
        val14 = self.get_total_payment_customer()
        val15 = self.get_total_bill_payment()
        val16 = self.get_product_available()
        val17 = self.get_employees()
        val18 = self.get_expenses()
        val19 = self.get_total_receipt()
        val20 = self.get_total_delivery()
        val21 = self.get_today_receipt(current_date)
        val22 = self.get_today_delivery(current_date)
        res['total_sale_order'] = val2
        res['today_sale_order'] = val1
        res['today_invoice'] = val3
        res['today_purchase_order'] = val8
        res['total_purchase'] = val9
        res['total_invoice'] = val6
        res['total_vendors'] = val5
        res['total_products'] = val7
        res['total_customers'] = val4
        res['today_payment_received'] = val10
        res['total_bill'] = val11
        res['today_bill_payment'] = val12
        res['today_bill'] = val13
        res['total_payment_customer'] = val14
        res['total_bill_payment'] = val15
        res['product_available'] = val16
        res['total_employees'] = val17
        res['total_expenses'] = val18
        res['total_receipts'] = val19
        res['total_delivery'] = val20
        res['today_receipt'] = val21
        res['today_delivery'] = val22
        return res

    def get_today_sale_order(self, date):
        sale_order = self.env['sale.order'].search([])
        today_sale_order = 0
        for rec in sale_order:
            if rec.date_order.date() == date:
                today_sale_order += 1
        return today_sale_order

    def get_total_sale_order(self):
        sale_order = self.env['sale.order']
        total_sale_order = sale_order.search([])
        return len(total_sale_order)

    def get_today_invoice(self, date):
        today_invoice = self.env['account.invoice'].search([('type', '=', 'out_invoice')])
        today_invoice_val = 0
        for rec in today_invoice:
            if rec.date_invoice == date:
                today_invoice_val += 1
        return today_invoice_val

    def get_total_invoice(self):
        total_invoice = self.env['account.invoice']
        total_invoice_val = total_invoice.search([('type', '=', 'out_invoice')])
        return len(total_invoice_val)

    def get_today_purchase(self, date):
        today_order_purcahse = self.env['purchase.order'].search([])
        today_purchase_order_val = 0
        for rec in today_order_purcahse:
            if rec.date_order.date() == date:
                today_purchase_order_val += 1
        return today_purchase_order_val

    def get_total_purchase(self):
        total_purchase = self.env['purchase.order']
        total_purchase_val = total_purchase.search([])
        return len(total_purchase_val)

    def get_total_products(self):
        total_products = self.env['product.template']
        total_product_val = total_products.search([])
        return len(total_product_val)

    def get_total_vendors(self):
        total_vendors = self.env['res.partner']
        total_vendor_val = total_vendors.search([])
        return len(total_vendor_val)

    def get_total_customers(self):
        total_customers = self.env['res.partner']
        total_customer_val = total_customers.search([])
        return len(total_customer_val)

    def get_today_payment_received(self, date):
        today_payment_received = self.env['account.invoice'].search([('type', '=', 'out_invoice')])
        total = 0
        for rec in today_payment_received:
            if rec.date_invoice == date:
                total_invoices = rec.amount_total
                total = total + total_invoices
        return total

    def get_today_bill_payment(self, date):
        today_payment_bill = self.env['account.invoice'].search([('type', '=', 'in_invoice')])
        total = 0
        for rec in today_payment_bill:
            if rec.date_invoice == date:
                total_bill_invoices = rec.amount_total
                total = total + total_bill_invoices
        return total

    def get_total_bills(self):
        total_bill = self.env['account.invoice'].search([('type', '=', 'in_invoice')])
        return len(total_bill)

    def get_today_bill(self, date):
        today_bill = self.env['account.invoice'].search([('type', '=', 'in_invoice')])
        today_bill_val = 0
        for rec in today_bill:
            if rec.date_invoice == date:
                today_bill_val += 1
        return today_bill_val

    def get_total_payment_customer(self):
        total_payment_customer = self.env['account.invoice'].search([('type', '=', 'out_invoice')])
        total = 0
        for rec in total_payment_customer:
            total_invoices_customer = rec.amount_total
            total = total + total_invoices_customer
        return total

    def get_total_bill_payment(self):
        total_payment_bill = self.env['account.invoice'].search([('type', '=', 'in_invoice')])
        total = 0
        for rec in total_payment_bill:
            total_bill_invoices = rec.amount_total
            total = total + total_bill_invoices
        return total

    def get_product_available(self):
        total_product_available = self.env['product.template'].search([('qty_available', '>', 0)])
        return len(total_product_available)

    def get_employees(self):
        total_employees = self.env['hr.employee'].search([])
        return len(total_employees)

    def get_expenses(self):
        total_expenses = self.env['hr.expense'].search([])
        return len(total_expenses)

    def get_id_incoming_picking_type(self):
        stock_picking_type = self.env['stock.picking.type'].search([('code', '=', 'incoming')])
        for rec in stock_picking_type:
            return rec.id

    def get_id_outgoing_picking_type(self):
        stock_picking_type = self.env['stock.picking.type'].search([('code', '=', 'outgoing')])
        for rec in stock_picking_type:
            return rec.id

    def get_total_receipt(self):
        picking_type_id = self.get_id_incoming_picking_type()
        receipts = self.env['stock.picking'].search([('picking_type_id', '=', picking_type_id)])
        return len(receipts)

    def get_total_delivery(self):
        picking_type_id = self.get_id_outgoing_picking_type()
        delivery = self.env['stock.picking'].search([('picking_type_id', '=', picking_type_id)])
        return len(delivery)

    def get_today_receipt(self, date):
        today_receipt = self.env['stock.picking'].search([('picking_type_id', '=', self.get_id_incoming_picking_type())])
        today_receipt_val = 0
        for rec in today_receipt:
            if rec.scheduled_date == date:
                today_receipt_val += 1
        return today_receipt_val

    def get_today_delivery(self, date):
        today_delivery = self.env['stock.picking'].search([('picking_type_id', '=', self.get_id_outgoing_picking_type())])
        today_delivery_val = 0
        for rec in today_delivery:
            if rec.date_done == date:
                today_delivery_val += 1
        return today_delivery_val

    def action_view_data(self):
        domain = []
        _name = ''
        context = self._context.copy()
        current_date = date.today()
        today = fields.Date.context_today(self).strftime('%Y-%m-%d')
        if self._context.get('today_sale_order'):
            domain = [('date_order', '=', (datetime.today().date()).strftime('%Y-%m-%d')), ('date_order', '=', (datetime.today().date()).strftime('%Y-%m-%d'))]
            _name = 'Sale Order'
            model = 'sale.order'
            rq_tree = self.env.ref('sale.view_quotation_tree_with_onboarding', False)
            rq_form = self.env.ref('sale.view_order_form', False)
        if self._context.get('today_invoice'):
            domain = [('type', '=', 'out_invoice'), ('date_invoice', '=', today)]
            _name = 'Today Invoice'
            model = 'account.invoice'
            rq_tree = self.env.ref('account.invoice_tree_with_onboarding', False)
            rq_form = self.env.ref('account.invoice_form', False)
        if self._context.get('total_invoice'):
            domain = [('type', '=', 'out_invoice')]
            _name = 'Invoice'
            model = 'account.invoice'
            rq_tree = self.env.ref('account.invoice_tree_with_onboarding', False)
            rq_form = self.env.ref('account.invoice_form', False)
        if self._context.get('total_bill'):
            domain = [('type', '=', 'in_invoice')]
            _name = 'Bill'
            model = 'account.invoice'
            rq_tree = self.env.ref('account.invoice_tree_with_onboarding', False)
            rq_form = self.env.ref('account.invoice_form', False)
        if self._context.get('total_customers'):
            domain = []
            _name = 'Customers'
            model = 'res.partner'
            rq_tree = self.env.ref('base.view_partner_tree', False)
            rq_form = self.env.ref('base.view_partner_form', False)
        if self._context.get('total_vendors'):
            domain = []
            _name = 'Vendors'
            model = 'res.partner'
            rq_tree = self.env.ref('base.view_partner_tree', False)
            rq_form = self.env.ref('base.view_partner_form', False)
        if self._context.get('total_product_template'):
            domain = []
            _name = 'Product Template'
            model = 'product.template'
            rq_tree = self.env.ref('product.product_template_tree_view', False)
            rq_form = self.env.ref('product.product_template_only_form_view', False)
        if self._context.get('total_product_available'):
            domain = [('qty_available', '>', 0)]
            _name = 'Product Template'
            model = 'product.template'
            rq_tree = self.env.ref('product.product_template_tree_view', False)
            rq_form = self.env.ref('product.product_template_only_form_view', False)
        if self._context.get('total_purchase_order'):
            domain = []
            _name = 'Purchase Order'
            model = 'purchase.order'
            rq_tree = self.env.ref('purchase.purchase_order_tree', False)
            rq_form = self.env.ref('purchase.purchase_order_form', False)

        if self._context.get('total_sale_order'):
            domain = []
            _name = 'Sale Order'
            model = 'sale.order'
            rq_tree = self.env.ref('sale.view_quotation_tree_with_onboarding', False)
            rq_form = self.env.ref('sale.view_order_form', False)
        if self._context.get('total_expenses'):
            domain = []
            _name = 'Expenses'
            model = 'hr.expense'
            rq_tree = self.env.ref('hr_expense.view_expenses_tree', False)
            rq_form = self.env.ref('hr_expense.hr_expense_view_form', False)
        if self._context.get('total_employees'):
            domain = []
            _name = 'Employees'
            model = 'hr.employee'
            rq_tree = self.env.ref('hr.view_employee_tree', False)
            rq_form = self.env.ref('hr.view_employee_form', False)
        if self._context.get('total_delivery'):
            domain = [('picking_type_id', '=', self.get_id_outgoing_picking_type())]
            _name = 'Delivery'
            model = 'stock.picking'
            rq_tree = self.env.ref('stock.vpicktree', False)
            rq_form = self.env.ref('stock.view_picking_form', False)
        if self._context.get('total_receipt'):
            domain = [('picking_type_id', '=', self.get_id_incoming_picking_type())]
            _name = 'Receipt'
            model = 'stock.picking'
            rq_tree = self.env.ref('stock.vpicktree', False)
            rq_form = self.env.ref('stock.view_picking_form', False)
        if rq_tree:
            views = []
            if rq_tree and rq_form:
                views = [(rq_tree.id, 'tree'), (rq_form.id, 'form')]
            else:
                views = [(rq_tree.id, 'tree')]
            return {
                'name': _name,
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree',
                'res_model': model,
                'views': views,
                'view_id': rq_tree.id,
                'target': '',
                'context': context,
                'domain': domain,
            }

    def reset_fields(self):
        for record in self:
            if record.sale_order_number:
                record.sale_order_number = ''
            if record.invoice_number:
                record.invoice_number = ''
            if record.customer_name:
                record.customer_name = ''
            if record.customer_phone:
                record.customer_phone = ''

    @api.onchange('sale_order_number')
    def get_search_data_sale(self):
        search_domain = []
        if self.sale_order_number:
            search_domain += [('id', '=', self.sale_order_number.id)]

            sale_rec = self.env['sale.order'].search(search_domain)
            if sale_rec:
                self.search_line_ids = [(6, 0, sale_rec.ids)]
            else:
                raise ValidationError('No Data Found')

    @api.onchange('invoice_number')
    def get_search_data_invoice(self):
        search_domain = []
        if self.invoice_number:
            search_domain += [('id', '=', self.invoice_number.id)]

            invoice_rec = self.env['account.invoice'].search(search_domain)
            if invoice_rec:
                self.search_line_ids1 = [(6, 0, invoice_rec.ids)]
            else:
                raise ValidationError('No Data Found')

    @api.onchange('customer_name')
    def get_search_data_customer(self):
        search_domain = []
        if self.customer_name:
            search_domain += [('id', '=', self.customer_name.id)]

            customer_rec = self.env['res.partner'].search(search_domain)
            if customer_rec:
                self.search_line_ids2 = [(6, 0, customer_rec.ids)]
            else:
                raise ValidationError('No Data Found')




