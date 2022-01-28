import json
import logging
from hashlib import sha256

# import urlparse

import dateutil.parser
import pytz

from odoo import api, fields, models, _
from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.tools.float_utils import float_compare
from urllib.parse import urlparse,urljoin

_logger = logging.getLogger(__name__)

class ResCurrency(models.Model):
    _inherit='res.currency'

    currency_code=fields.Char('Currency Code')

class PaymentAcquirerPaycap(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('paycaps', 'Paycaps')],ondelete={'paycaps': 'set default'})
    app_id = fields.Char('APP ID', required_if_provider='paycaps', groups='base.group_user')
    secret_key = fields.Char('Secret Key', required_if_provider='paycaps', groups='base.group_user')

    def _get_paycaps_urls(self):
        """ PayUmoney URLs"""
        if self.state == 'enabled':
            return {'paycaps_form_url': 'https://secure.paycaps.com/pgui/jsp/paymentrequest'}
        else:
            return {'paycaps_form_url': 'https://sandbox.paycaps.com/pgui/jsp/paymentrequest'}

    #@api.multi
    def paycaps_get_form_action_url(self):
        return self._get_paycaps_urls()['paycaps_form_url']


    #@api.multi
    def generate_hash(self,params):
        params_string = []
        secret_key =getattr(self, 'secret_key')#'1a912bc2dab245df'
        print("777777777",secret_key)
        for key in sorted(params.keys()):
            value = '='.join([str(key), str(params[key])])
            params_string.append('' if value == 'null' else str(value))
        
        # Join all values in single string
        params_string = '~'.join(params_string)

        # Add Salt
        final_string = '%s%s' % (params_string, secret_key)
        print('final_stringfinal_string',final_string)
        # Generate 256 hash
        hasher = sha256(final_string.encode())
        hash_string = hasher.hexdigest().upper()
        print("hash_stringhash_stringhash_stringhash_string",hash_string)
        return hash_string

    #@api.multi
    def paycaps_form_generate_values(self, values):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        currency_id=self.env['res.currency'].sudo().search([('id','=',values['currency_id'])])

        # currency_id = values['currency']
        # currency = currency_id
        reference = values['reference'].split('-')
        reference = reference[0]
        if values['reference']:
            merchant_reference = values['reference']

        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        ## all values
        APP_ID = getattr(self, 'app_id')#'1000210207170917'
        MERCHANTNAME='NT Demo'
        ORDER_ID =reference #'NT000014'
        RETURN_URL='%s' % urljoin(base_url,'/shop/confirmation')
        CUST_EMAIL =values['partner_email']
        CUST_NAME=values['partner_name']
        CUST_STREET_ADDRESS1=values['partner_address']
        CUST_CITY=values['partner_city']
        CUST_STATE='Dubai'
        CUST_ZIP=values['partner_zip']
        CUST_PHONE =values['partner_phone']
        CURRENCY_CODE=currency_id.currency_code#values['currency_id']#'784'
        AMOUNT =round(int(values['amount'] * 100), 2)
        TXNTYPE='SALE' 
    
        data = {}
        data["APP_ID"] = APP_ID
        data["ORDER_ID"] = ORDER_ID
        data["RETURN_URL"] = RETURN_URL
        data["CUST_EMAIL"] = CUST_EMAIL
        data["CUST_NAME"] = CUST_NAME
        data["CUST_STREET_ADDRESS1"] =CUST_STREET_ADDRESS1
        #data["CUST_CITY"] = CUST_CITY
        #data["CUST_STATE"] = 'Dubai'
        #data["CUST_COUNTRY"] = "NA"
        data["CUST_ZIP"] = CUST_ZIP
        data["CUST_PHONE"] = CUST_PHONE
        data["CURRENCY_CODE"] = CURRENCY_CODE
        data["AMOUNT"] = AMOUNT
        data["PRODUCT_DESC"] = "Test Transaction"
        #data["CUST_SHIP_STREET_ADDRESS1"] = CUST_STREET_ADDRESS1
        #data["CUST_SHIP_CITY"] =CUST_CITY
        #data["CUST_SHIP_STATE"] = CUST_STATE
        #data["CUST_SHIP_COUNTRY"] = "NA"
        #data["CUST_SHIP_ZIP"] = CUST_ZIP
       # data["CUST_SHIP_PHONE"] = CUST_PHONE
        #data["CUST_SHIP_NAME"] = CUST_NAME
        data["TXNTYPE"] = TXNTYPE

        data["HASH"] = self.generate_hash(data)
        paycaps_tx_values = dict(values)
        paycaps_tx_values.update({
            "AMOUNT": AMOUNT,
            "APP_ID": APP_ID, 
            "ORDER_ID":ORDER_ID ,          
            "CURRENCY_CODE":CURRENCY_CODE,#"784", 
            "CUST_NAME":CUST_NAME,
            "CUST_EMAIL":CUST_EMAIL,
            "CUST_PHONE":CUST_PHONE,
            "CUST_STREET_ADDRESS1":CUST_STREET_ADDRESS1,
            "CUST_ZIP":CUST_ZIP,            ''          
            "HASH": data["HASH"],#signature.upper(),
            "PRODUCT_DESC":"NT Demo Transaction",
            "RETURN_URL":RETURN_URL,
            "TXNTYPE":TXNTYPE, 
           
        })
        return paycaps_tx_values
