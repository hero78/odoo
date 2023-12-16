# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
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
{
  "name"                 :  "Website Cinetpay Checkout Payment Acquirer",
  "summary"              :  """Website CinetPay Checkout Payment Acquirer enables seamless online payments by integrating CinetPay's secure and versatile payment gateway. With CinetPay Payment Acquirer or simply a payment acquirer, businesses can offer their customers a smooth and secure checkout experience, enhancing overall transaction efficiency.""",
  "category"             :  "Website",
  "version"              :  "1.0.1",
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://webkul.com/blog/guide-for-odoo-website-cinetpay-checkout-payment-acquirer/",
  "description"          :  """Streamline your checkout process with Odoo Website CinetPay Checkout Payment Acquirer. Enjoy easy payments and enhanced user experience.
                               Cinetpay Acquirer For Odoo Checkout
                               Odoo Cinetpay Integration: Pay With Ease
                               Odoo Cinetpay Acquirer, Cinetpay Acquirer
                               Odoo Cinetpay Payment Integration
                               Cinetpay Payment Acquirer For Odoo
                               Odoo, Odoo Apps, Odoo Admin
                               Odoo Payment Acquirer
                               Odoo Payment Gateway
                               Payment Acquirer
                               Payment Gateway
                               Odoo Website
                               Odoo Website Cinetpay Checkout Payment Acquirer
                              """,
  "depends"              :  ['payment'],
  "data"                 :  [
                             'views/payment_cinetpay_templates.xml',
                             'views/payment_views.xml',
                             'data/cinetpay_checkout_demo_data.xml',
                            ],
  "images"               :  ['static/description/Banner.gif'],
  "application"          :  True,
  "installable"          :  True,
  "price"                :  99,
  "currency"             :  "USD",
  "pre_init_hook"        :  "pre_init_check",
  "post_init_hook"       :  "post_init_hook",
  "uninstall_hook"       :  "uninstall_hook",
}
