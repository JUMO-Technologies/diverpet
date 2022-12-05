from odoo import models, fields, api


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    @api.model
    def default_get(self, fields_list):
        res = super(MailComposeMessage, self).default_get(fields_list)
        if res.get('res_id') and res.get('model') and \
                res.get('composition_mode', '') != 'mass_mail' and\
                not res.get('can_attach_attachment'):
            res['can_attach_attachment'] = True  # pragma: no cover
        return res

    @api.model
    def _get_object_attachment_domain(self):
        return "[('res_model', '=', model), ('res_id', '=', res_id)]"

    can_attach_attachment = fields.Boolean(string='Can Attach Attachment')
    object_attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        relation='mail_compose_message_ir_attachments_object_rel',
        column1='wizard_id', column2='attachment_id', string='Attachments',
        domain=lambda self: self._get_object_attachment_domain())

    def get_mail_values(self, res_ids):
        res = super(MailComposeMessage, self).get_mail_values(res_ids)
        if self.object_attachment_ids.ids and self.model and len(res_ids) == 1:
            res[res_ids[0]].setdefault('attachment_ids', []).extend(
                self.object_attachment_ids.ids)
        return res
