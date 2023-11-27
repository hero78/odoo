# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.addons.payment.tests.common import PaymentCommon


class PaymentCinetpayCommon(PaymentCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.provider = cls._prepare_provider(code='cinetpay')

        cls.notification_data = {
            'reference': cls.reference,
            'payment_details': '1234',
            'simulated_state': 'done',
        }
