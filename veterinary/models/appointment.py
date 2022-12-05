from odoo import models, fields, api, _
from odoo import tools


class AccountMove(models.Model):
    _inherit = 'account.move'

    def app_id_auto(self):
        try:
            return self._context.get('active_ids')[0]
        except Exception:
            return False

    appointment_id = fields.Many2one('veterinary.appointment', default=lambda self: self.app_id_auto())


class Appointment(models.Model):
    _name = 'veterinary.appointment'
    _description = "Veterinary Appointment"
    _order = 'dateOfAppointment desc'

    cancel_reason = fields.Text('Reason of cancellation')
    description = fields.Char('Description')
    dateOfAppointment = fields.Datetime('Date of Appointment', required=True)
    name = fields.Char(string='Name', readonly=True, default=lambda self: _('New'))
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirm', 'Confirm'),
         ('cancel', 'Cancel')], string='Status', index=True, readonly=True, default='draft',
        tracking=True, copy=False)
    total_invoiced = fields.Char('Total', compute='_total_count')

    animals = fields.Many2many('veterinary.animal', string='Animals')
    animal_id = fields.Many2one('veterinary.animal')
    user_id = fields.Many2one('res.users', string='Doctor', required=True,
                              tracking=True, default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string='Owner', required=True)
    invoice_ids = fields.One2many('account.move', 'appointment_id', string="Appointment Id")

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('appointment.number') or _('New')
        res = super(Appointment, self).create(vals)
        return res

    def action_create_invoice(self):
        for appointment in self:
            inv = {
                'appointment_id': appointment.id,
                'partner_id': appointment.partner_id.id,
                'move_type': 'out_invoice',
            }
            invoiced = self.env['account.move'].create(inv)
            return self.invoice_view()

    def _total_count(self):
        t = self.env['account.move'].search([['appointment_id', '=', self.id]])
        self.total_invoiced = len(t)

    def action_cancel_appointment(self):
        return self.write({'state': 'cancel'})

    def invoice_view(self):
        action = self.env.ref('account.action_move_out_refund_type')
        result = action.read()[0]
        result['domain'] = [('appointment_id', '=', self.id)]
        return result

    def action_confirm(self):
        self.state = 'confirm'
        for animal in self.animals:
            pick = {
                'animal': animal.id,
                'appointment_id': self.id,
                'partner_id': self.partner_id.id,
            }
            picking = self.env['veterinary.evaluation'].create(pick)
        return self.invoice_view()
