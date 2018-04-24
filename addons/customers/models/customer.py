# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource

class CustomerTeam(models.Model):

    _name = "customer.team"
    _description = "Customer Team"

    name = fields.Char(string="Team Name", required=True)
    customer_ids = fields.Many2many('res.partner', string='Customers')

    # _sql_constraints = [
    #     ('name_uniq', 'unique (name)', "Tag name already exists !"),
    # ]
