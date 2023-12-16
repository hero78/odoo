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
import hmac
import hashlib
import pprint
import logging
_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('cinetpay_checkout', 'CinetPay Checkout')],ondelete={'cinetpay_checkout': 'cascade'})
    cinetpay_api_key = fields.Char("Api key", required_if_provider='cinetpay_checkout', help="Enter cinetpay api key.")
    cinetpay_site_id = fields.Char("Site_id", required_if_provider='cinetpay_checkout', help="Enter cinetpay site_id.")

    def _cinetpay_get_api_url(self):
        """ Return the API URL according to the acquirer state.
        Note: self.ensure_one()
        :return: The API URL
        :rtype: str
        """
        self.ensure_one()
        return '/payment/cinetpay/gateway'
