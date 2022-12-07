import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class ProductPricelistDetail(models.Model):
    _name = 'product.pricelist.detail'

    pricelist_id = fields.Many2one('product.pricelist', string="Pricelist")

    product_id = fields.Many2one('product.product', string="Product")

    manual_price = fields.Boolean(string="Manual Price", default=False)

    product_tmpl_id = fields.Many2one('product.template', string="Product Template")

    price = fields.Float(string="Price", digits='Product Price')

    def write(self, vals_list):
        res = super(ProductPricelistDetail, self).write(vals_list)
        for rec in self:
            if rec.manual_price:
                #buscar producto en pricelist item
                dominio = [('pricelist_id', '=', rec.pricelist_id.id),
                                                                  ('product_tmpl_id', '=', rec.product_tmpl_id.id),
                                                                  ('compute_price', '=', 'fixed'),
                                                                  ('applied_on', '=', '1_product')]
                if rec.product_id:
                    dominio = [('pricelist_id', '=', rec.pricelist_id.id),
                               ('product_id', '=', rec.product_id.id),
                               ('compute_price', '=', 'fixed'),
                               ('applied_on', '=', '0_product_variant')]
                item = self.env['product.pricelist.item'].search(dominio)
                if item:
                    item.fixed_price = rec.price
                else:
                    #crear pricelist item
                    data = {'pricelist_id': rec.pricelist_id.id, 'product_tmpl_id': rec.product_tmpl_id.id, 'compute_price': 'fixed',
                        'fixed_price': rec.price, 'applied_on': '1_product'}
                    if rec.product_id:
                        data = {'pricelist_id': rec.pricelist_id.id,
                                'product_id': rec.product_id.id,
                                'compute_price': 'fixed',
                                'fixed_price': rec.price,
                                'applied_on': '0_product_variant'}
                    self.env['product.pricelist.item'].create(data)
        return res
