# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
import odoo
from odoo import http, _,exceptions
from odoo.http import request, Response
import urllib.request
import requests
import werkzeug
import json
import pprint
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class CinetpayCheckout(http.Controller):
    _return_url = '/payment/cinetpay/checkout/return'
    _cancel_url = '/payment/cinetpay/checkout/cancel'
    _webhook_url = '/payment/cinetpay/checkout/webhook'

    def _check_status(self,token):
        trans_obj = request.env['payment.transaction'].sudo().search([('cinetpay_payment_token','=',token)],limit=1)
        headers = {
            "Content-Type" : "application/json",
        }
        if trans_obj:
            payload = {
                        'apikey':trans_obj.provider_id.cinetpay_api_key,
                        'site_id' :trans_obj.provider_id.cinetpay_site_id,
                        'token' : trans_obj.cinetpay_payment_token
                        }
            data = json.dumps(payload)
            response = requests.post('https://api-checkout.cinetpay.com/v2/payment/check', data=data, headers=headers)
            res_data = response.json()
            try:
                request.env['payment.transaction'].sudo()._handle_notification_data('cinetpay_checkout', res_data)
            except Exception as e:
                _logger.warning("Exception ====From===Cinetpay==Check==status======%r",e)
            #res_data.get('data').update({'status':'ACCEPTED'})
            return res_data
        else:
            raise ValidationError(
                "CinetPay: " + _("Transaction record not found ")
            )


    @http.route(['/payment/cinetpay/gateway',], type='http', auth="public", website=True)
    def payment_cinetpay_gateway(self, **post):
        headers = {
            "Content-Type" : "application/json",
        }
        trans_id = post.get('description')
        trans_obj = request.env['payment.transaction'].sudo().search([('reference','=',trans_id)])
        data = json.dumps(post)
        response = requests.post('https://api-checkout.cinetpay.com/v2/payment', data=data, headers=headers)
        res_data = response.json()
        try:
            if trans_obj:
                trans_obj.cinetpay_payment_token = res_data.get('data').get('payment_token')
                return werkzeug.utils.redirect(res_data.get('data').get("payment_url"))
        except Exception as e:
            raise ValidationError(
                "CinetPay: " + _("%s.", res_data.get('description'))
            )


    @http.route(_return_url, type='http', auth="public", csrf=False, save_session=False)
    def cinetpay_checkout_return(self, **post):
        token = post.get('token')
        payload = self._check_status(token)
        return werkzeug.utils.redirect('/payment/status')

    @http.route(_webhook_url, type='http', methods=['GET', 'POST'], csrf=False, auth='public')
    def cinetpay_checkout_webhook(self,**data):
        reference = data.get('cpm_designation')
        trans_obj = request.env['payment.transaction'].sudo().search([('reference','=',reference)],limit=1)
        payload = self._check_status(trans_obj.cinetpay_payment_token)
        if payload.get('data').get('status') == 'ACCEPTED' :
            trans_obj._reconcile_after_done()
            orders = trans_obj.sale_order_ids
            for order in orders:
               order.sudo().action_done()
        return ''
