# -*- coding: utf-8 -*-

from . import models

# import base_config_settings
import decimal_precision

# don't try to be a good boy and sort imports alphabetically.
# `product.template` should be initialised before `product.product`
import product_template
import product

# import product_attribute
# import product_pricelist
import product_uom
# import res_company
# import res_partner