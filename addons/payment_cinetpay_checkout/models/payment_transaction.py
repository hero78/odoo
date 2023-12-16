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
from odoo import _, api, fields, models
from odoo.addons.payment import utils as payment_utils
from odoo.exceptions import UserError, ValidationError
from odoo.addons.payment_cinetpay_checkout.controllers.main import CinetpayCheckout
from odoo.http import request
from werkzeug import urls
from math import floor
from random import random
import pprint
import requests
import json
import logging
_logger = logging.getLogger(__name__)


PAYMENT_STATUS_MAPPING = {
    'pending': ('WAITING_FOR_CUSTOMER'),
    'authorized': ('authorized'),
    'done': ('ACCEPTED'),
    'cancel': ('REFUSED'),
}

class TransactionCinetpayCheckout(models.Model):
    _inherit = 'payment.transaction'

    cinetpay_payment_token = fields.Char("cinetpay payment token")
    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'cinetpay_checkout':
            return res
        base_url = self.provider_id.get_base_url()
        payment_acquirer = self.provider_id
        remaining = self.amount%5
        if not remaining:
            amount = self.amount
        else:
            amount = self.amount+(5-remaining)
        phone_no = ''.join(e for e in str(self.partner_phone) if e.isalnum() or e == '+')
        data = {
        "apikey"  : self.provider_id.cinetpay_api_key,
        "site_id" : self.provider_id.cinetpay_site_id,
        "transaction_id" : str(floor(random() * 100000000)),
        "amount" : amount,
        "currency": self.currency_id.name,
        "description" : self.reference,
        "notify_url"    : urls.url_join(base_url, CinetpayCheckout._webhook_url),
        "return_url"   :  urls.url_join(base_url, CinetpayCheckout._return_url),
        "channels"   :   'ALL',
        "customer_name"   :  self.partner_name ,
        "customer_surname"   :   self.partner_name,
        "customer_phone_number"   :   phone_no,
        "customer_email"   :    self.partner_email,
        "customer_address"   :   self.partner_address,
        "customer_city"   :      self.partner_city,
        "customer_country"   :   self.partner_country_id.code,
        "customer_state"      :  self.partner_state_id.code,
        "customer_zip_code"   :  self.partner_zip,
        "api_url"   : self.provider_id._cinetpay_get_api_url(),
        }
        return data


    @api.model
    def _get_tx_from_notification_data(self, provider, data):
        """ Given a data dict coming from CinetPay, verify it and find the related
        transaction record. Create a payment method if an alias is returned."""
        res = super()._get_tx_from_feedback_data(provider,data)
        if provider != "cinetpay_checkout":
            return res
        reference = data.get('data').get("description")
        tx = self.sudo().search([('reference','=',reference),('provider','=','cinetpay_checkout')],limit=1)
        if not tx:
            raise ValidationError(
                "CinetPay: " + _("No transaction found matching cinetpay transaction_id %s.", reference)
            )
        return tx

    def _process_notification_data(self, data):
        res = super()._process_feedback_data(data)
        if self.provider != 'cinetpay_checkout':
            return res
        payment_status = data.get('data').get('status')
        if payment_status in PAYMENT_STATUS_MAPPING['pending']:
            self._set_pending(state_message=data.get('pending_reason'))
        elif payment_status in PAYMENT_STATUS_MAPPING['authorized']:
            self._set_authorized()
        elif payment_status in PAYMENT_STATUS_MAPPING['done']:
            self._set_done()
        elif payment_status in PAYMENT_STATUS_MAPPING['cancel']:
            self._set_error("Cinetpay: "+_("Sorry transaction failed for this order."))
        else:
            self._set_error(
                "Cinetpay: " + _("Received data with invalid payment status: %s", payment_status)
            )

    def _finalize_post_processing(self):
        orders = self.sale_order_ids
        for order in orders:
           if order.invoice_count != 0:
              return False
        super()._finalize_post_processing()
