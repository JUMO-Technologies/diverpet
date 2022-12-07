import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = 'product.product'

    def get_pricelists(self):
        for rec in self:
            pricelist_ids = self.env['product.pricelist'].search([('show_on_products', '=', True)])
            details = [(5, 0, 0)]
            print(pricelist_ids)
            for pricelist in pricelist_ids:
                price = pricelist._get_product_price(rec, 1.0)
                l_actuales = self.env['product.pricelist.detail'].search(
                    [('product_id', '=', rec.id), ('pricelist_id', '=', pricelist.id)])
                if l_actuales:
                    l_actuales.unlink()
                l = self.env['product.pricelist.detail'].create(
                    {'pricelist_id': pricelist.id, 'product_id': rec.id, 'price': price})
                details.append((4,l.id))
            rec.pricelists = details

    pricelists = fields.One2many(
            'product.pricelist.detail',
            string="Pricelists",
            compute="get_pricelists"
    )