import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    pricelist_ids = fields.One2many('product.pricelist.item', 'product_id')
