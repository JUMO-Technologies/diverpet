from odoo import models, fields, api, _
from odoo import tools


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.depends('product_id', 'journal_id')
    def _compute_name(self):
        for line in self:
            if line.display_type == 'payment_term':
                if line.move_id.payment_reference:
                    line.name = line.move_id.payment_reference
                elif not line.name:
                    line.name = ''
                continue
            if not line.product_id or line.display_type in ('line_section', 'line_note'):
                continue
            if line.partner_id.lang:
                product = line.product_id.with_context(lang=line.partner_id.lang)
            else:
                product = line.product_id

            values = []
            if product.partner_ref:
                values.append(product.partner_ref)
            # if line.journal_id.type == 'sale':
            #     if product.description_sale:
            #         values.append(product.description_sale)
            # elif line.journal_id.type == 'purchase':
            #     if product.description_purchase:
            #         values.append(product.description_purchase)
            line.name = '\n'.join(values)