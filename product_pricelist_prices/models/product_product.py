import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    pricelist_ids = fields.One2many('product.pricelist.item', 'product_id')

    # override to delete description_sale
    def get_product_multiline_description_sale(self):
        name = self.display_name

        return name
