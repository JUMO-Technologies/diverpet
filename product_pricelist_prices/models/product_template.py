# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'


    def get_pricelists(self):
        for rec in self:
            pricelist_ids = self.env['product.pricelist'].search([('show_on_products', '=', True)])
            details = []
            if not len(rec.product_variant_ids) > 1:
                for pricelist in pricelist_ids:
                    price = pricelist._get_product_price(rec, 1.0)
                    #l_actuales = self.env['product.pricelist.detail'].search([('product_tmpl_id', '=', rec.id), ('pricelist_id', '=', pricelist.id)])
                    l_actuales = rec.pricelists.filtered(lambda x: x.pricelist_id.id == pricelist.id)
                    if l_actuales:
                        l_actuales.write({'price': price})
                    else:
                        l = self.env['product.pricelist.detail'].create({'pricelist_id': pricelist.id, 'product_tmpl_id': rec.id, 'price': price})
                        details.append((4,l.id))
            rec.write({'pricelists': details})

    def _get_pricelists(self):
        self.pricelists = self.env['product.pricelist'].search(
                [
                    ('show_on_products', '=', True)
                ]
        )


    def _set_pricelists(self):
        for pricelist in self.pricelists:
            if pricelist.product_price:
                _logger.debug("Updating Price: %s", pricelist.product_price)
                pricelist.price_set(self, pricelist.product_price)

    pricelists = fields.One2many(
            'product.pricelist.detail',
            string="Pricelists",
            compute="get_pricelists", readonly=False
    )
