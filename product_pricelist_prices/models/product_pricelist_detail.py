import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class ProductPricelistDetail(models.Model):
    _name = 'product.pricelist.detail'

    pricelist_id = fields.Many2one('product.pricelist', string="Pricelist")

    product_id = fields.Many2one('product.product', string="Product")

    product_tmpl_id = fields.Many2one('product.template', string="Product Template")

    price = fields.Float(string="Price", digits='Product Price')
