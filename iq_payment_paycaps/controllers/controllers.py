from werkzeug.utils import redirect

from odoo import http
from odoo.http import request
from odoo import api,models
from odoo.addons.website_sale.controllers.main import WebsiteSale
import datetime


class WebsiteSaleInherit(WebsiteSale):

    @http.route(['/shop/confirmation'], type='http', auth="public", website=True, csrf=False)
    def payment_confirmation(self, **post):
        print('\n\n\n <<<<<<<<<<< In payment_confirmation method of website_sale module [ CHILD ] >>>>>>>>>>\n\n\n')
        print('\npost 5645\n',post,'\n\n', request.session)
        if post:
            print("111111111111111111111111111111")
            if post.get('RESPONSE_CODE') =='300' and post.get('STATUS') == 'Invalid' :
                print("post.get('RESPONSE_CODE') ==300")
                data = {'response_message' : post.get('STATUS')}
                return request.render('payment_paycaps.paycaps_msg', data)

            elif post.get('RESPONSE_CODE') == '010' and post.get('STATUS') == 'Cancelled':
                data = {'response_message' : post.get('RESPONSE_MESSAGE')}
                return request.render('payment_paycaps.paycaps_msg', data)
            else:
                print("Sucess Paycaps")
                obj = http.request.env['account.journal'].sudo().search([('type', '=', 'bank')])
                for i in obj:
                    if i.name == 'Bank':
                        payment_type = i.id
                if post.get('RESPONSE_CODE') == '000' and post.get('RESPONSE_MESSAGE'):
                    account_acquirer_id = request.env['payment.acquirer'].sudo().search([('provider', '=', 'paycaps')],
                                                                                        limit=1)
                    if post['RESPONSE_MESSAGE'] == 'SUCCESS':
                        #reference = post['merchant_reference']
                        print("post['ORDER_ID']post['ORDER_ID']",post['ORDER_ID'])
                        reference = post['ORDER_ID']
                        sale_order_id =request.env['sale.order'].sudo().search([('name', '=', reference)])
                        order = request.env['sale.order'].sudo().search([('id', '=', sale_order_id.id)])
                        print('Order :',order)
                        print('\nsale_order_id :',sale_order_id)
                        if not order:
                            pay_link=request.env['account.move'].sudo().search([('name','=',reference)]).id
                            invoice_id= request.env['account.move'].sudo().search([('id', '=', pay_link)])
                            if invoice_id:
                                payment = http.request.env['sale.advance.payment.inv'].sudo().create({
                                    'advance_payment_method': 'delivered',
                                    'amount':int(post['AMOUNT'])/100,
                                })
                                payment_id = request.env['account.payment'].sudo().search(
                                    [('reconciled_invoice_ids', '=', invoice_id.id)], limit=1)
                                AccountPaymentRegister = request.env['account.payment.register'].with_context(
                                    active_ids=invoice_id.ids, active_model='account.move')
                                payment_obj = AccountPaymentRegister.sudo().create({
                                    'journal_id': account_acquirer_id.journal_id.id,
                                    'payment_method_id': request.env.ref(
                                        'payment.account_payment_method_electronic_in').id
                                })
                                payment_obj.action_create_payments()
                                if payment_id:
                                    payment_transaction_id = request.env['payment.transaction'].sudo().search(
                                        [('invoice_ids', '=', invoice_id.id)],
                                        limit=1)  # request.env['payment.transaction'].sudo().search([('reference','=',reference)],limit=1)
                                    if payment_transaction_id:
                                        payment_id.payment_transaction_id = payment_transaction_id.id
                                        payment_transaction_id.payment_id = payment_id.id
                                        payment_transaction_id.state = 'done'


                            return request.render("payment_paycaps.paycaps_confirmation_by_link", {'reference': reference})
                            hjghj
                        else:
                            context = {"active_model": 'sale.order', "active_ids": [order.id], "active_id": order.id}
                            amount = int(post['AMOUNT'])/100

                            for line in order.order_line:
                                print('order line product name :',line.product_id.name,line.product_id.id,line.product_id.invoice_policy)
                                if line.product_id.invoice_policy != 'order':
                                    print('In Iffffff')
                                    product = request.env['product.product'].sudo().browse(line.product_id.id)
                                    print('product',product)
                                    product.write({'invoice_policy' : 'order'})
                                    print('product.invoice_policy',product.invoice_policy)

                            order.action_confirm()

                            # Now create invoice.
                            payment = http.request.env['sale.advance.payment.inv'].sudo().create({
                                'advance_payment_method': 'delivered',
                                'amount': amount,
                            })
                            if not order.invoice_ids:
                                invoice = payment.with_context(context).create_invoices()
                                print("request.env.ref('payment.account_payment_method_electronic_in').sudo().id",
                                      request.env.ref('payment.account_payment_method_electronic_in').sudo().id)
                                for invoice in order.invoice_ids:
                                    invoice.with_context(context).action_post()
                                    AccountPaymentRegister = request.env['account.payment.register'].with_context(
                                        active_ids=invoice.ids, active_model='account.move')
                                    payment_obj = AccountPaymentRegister.sudo().create({
                                        'journal_id': account_acquirer_id.journal_id.id,
                                        'payment_method_id': request.env.ref(
                                            'payment.account_payment_method_electronic_in').id
                                    })
                                    payment_obj.action_create_payments()

                            if invoice:
                                payment_id = request.env['account.payment'].sudo().search(
                                    [('reconciled_invoice_ids', '=', invoice.id)], limit=1)
                                if payment_id:
                                    payment_transaction_id = request.env['payment.transaction'].sudo().search(
                                        [('invoice_ids', '=', invoice.id)],
                                        limit=1)  # request.env['payment.transaction'].sudo().search([('reference','=',reference)],limit=1)
                                    if payment_transaction_id:
                                        payment_id.payment_transaction_id = payment_transaction_id.id
                                        payment_transaction_id.payment_id = payment_id.id
                                        payment_transaction_id.state = 'done'
                                        # payment_id.action_cancel()
                                        # payment_id.action_draft()
                                        # payment_id.amount=invoice.amount_total
                                        # payment_id.action_post()

                                # fort_id = post.get('fort_id')
                                # invoice.write({'payfort_transaction_id' : fort_id})

                            request.website.sale_reset()

                        return request.render("payment_paycaps.paycaps_confirmation", {'order': order,'invoice':order.invoice_ids})

        else:
            print("###########3333333222222222222")
            if request.session['sale_last_order_id']:
                print("COD And wire transfer",)
                order = request.env['sale.order'].sudo().browse(request.session['sale_last_order_id'])
                return request.render("website_sale.confirmation", {'order': order})
            else:
                return request.redirect('/shop')


        
