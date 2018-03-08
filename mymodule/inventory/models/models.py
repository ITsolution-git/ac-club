# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_round
from datetime import datetime
import operator as py_operator

OPERATORS = {
    '<': py_operator.lt,
    '>': py_operator.gt,
    '<=': py_operator.le,
    '>=': py_operator.ge,
    '=': py_operator.eq,
    '!=': py_operator.ne
}

class Product(models.Model):
    _inherit = "product.product"
    _name = "stock.product"

    # reception_count = fields.Integer('Receipt', compute='_compute_reception_count')
    # delivery_count = fields.Integer('Delivery', compute='_compute_delivery_count')
    # stock_quant_ids = fields.One2many('stock.quant', 'product_id', help='Technical: used to compute quantities.')
    # stock_move_ids = fields.One2many('stock.move', 'product_id', help='Technical: used to compute quantities.')
    qty_available = fields.Float(
        'Quantity On Hand',
        digits=dp.get_precision('Product Unit of Measure'),
        help="Current quantity of products.\n"
             "In a context with a single Stock Location, this includes "
             "goods stored at this Location, or any of its children.\n"
             "In a context with a single Warehouse, this includes "
             "goods stored in the Stock Location of this Warehouse, or any "
             "of its children.\n"
             "stored in the Stock Location of the Warehouse of this Shop, "
             "or any of its children.\n"
             "Otherwise, this includes goods stored in any Stock Location "
             "with 'internal' type.")
    

class ProductChangeQuantity(models.TransientModel):
    _name = "stock.change.product.qty"
    _description = "Change Product Quantity"

    def _get_current_count(self):
        product_id = self.env.context.get('active_id')
        product = self.env['stock.product'].browse(product_id)	
        return product.qty_available

    product_id = fields.Many2one('stock.product', 'Product')

    new_quantity = fields.Float(
        'New Quantity on Hand', default=1,
        digits=dp.get_precision('Product Unit of Measure'), required=True,
        help='This quantity is expressed in the Default Unit of Measure of the product.')

    old_quantity = fields.Float(
        'Old Quantity on Hand', default=_get_current_count,
        digits=dp.get_precision('Product Unit of Measure'), required=True,
        help='This quantity is expressed in the Default Unit of Measure of the product.')


    @api.constrains('new_quantity')
    def check_new_quantity(self):
        if any(wizard.new_quantity < 0 for wizard in self):

            raise UserError(_('Quantity cannot be negative.'))

    @api.constrains('old_quantity')
    def check_old_quantity(self):
        if any(wizard.old_quantity < 0 for wizard in self):

            raise UserError(_('Quantity cannot be negative.'))

    def onchange_product_id_dict(self, product_id):
        return {
            'product_id': self.env['stock.product'].browse(product_id).id,
        }

    @api.model
    def create(self, values):
        # get product object
        product_id = self.env.context.get('active_id')
        print "pp" * 10
        print product_id
        product = self.env['stock.product'].browse(product_id)

        old_quantity = product.qty_available
        product.update({'qty_available': product.qty_available + values['new_quantity']})

        if values.get('product_id'):
            values.update(self.onchange_product_id_dict(values['product_id']))

        data = {'product_id': product_id, 'new_quantity': values['new_quantity'], 'old_quantity': old_quantity}
        return super(ProductChangeQuantity, self).create(data)

    @api.multi
    def change_product_qty(self):
        print "qq" * 10
        