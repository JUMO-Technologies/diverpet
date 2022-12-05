from odoo import models, fields, api, _
from ast import literal_eval


class Animal(models.Model):
    _name = 'veterinary.animal'
    _description = "Veterinary Animal"

    age = fields.Integer('Age', required=True)
    bread = fields.Selection(
        [('tb', 'TB'),
         ('ar', 'AR'),
         ('wb', 'WB'),
         ('p', 'P'),
         ('other', 'Other')], string="Breed & Use", required=True)
    colour = fields.Selection(
        [('b', 'B'),
         ('c', 'C'),
         ('g', 'G'),
         ('other', 'Other')], string="Colour", required=True)
    image = fields.Binary(
        "Image", attachment=True,
        help="This field holds the image used as image for the product, limited to 1024x1024px.")
    microchip_number = fields.Char('Microchip Number', required=True)
    name = fields.Char('Animal Name', required=True)
    sex = fields.Selection(
        [('f', 'F'),
         ('m', 'M'),
         ('g', 'G')], string="Sex", required=True)
    total_appointment = fields.Char('Total', compute='_total_appointment')

    # Relational Fields:
    appointment_id = fields.Many2many('veterinary.appointment')
    evaluation = fields.One2many('veterinary.evaluation', 'animal', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Owner', required=True)

    _sql_constraints = [
        ('microchio_uniq', 'unique(microchip_number)', 'Microchip already exists!')
    ]

    def _total_appointment(self):
        self.total_appointment = len(self.appointment_id)

    def appointment_view(self):
        action = self.env.ref('veterinary.action_appointment_form')
        result = action.read()[0]
        result['domain'] = [('animals', '=', self.id)]
        return result


class ResPartner(models.Model):
    _inherit = 'res.partner'

    animal_picking_id = fields.One2many('veterinary.animal', 'partner_id', string="Animal Id")

    def open_animal(self):
        action = self.env.ref('veterinary.action_animal_form')
        result = action.read()[0]
        result['domain'] = [('partner_id', '=', self.id)]
        return result
