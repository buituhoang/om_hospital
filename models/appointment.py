from odoo import api, models, fields, _
from datetime import datetime

from odoo.exceptions import UserError, ValidationError

class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Hospital Appointment"
    # _rec_name = "name"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "id desc"

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment.sequence') or _('New')
        result = super(HospitalAppointment, self).create(vals)
        return result

    def _get_default_note(self):
        return "Nothing"

    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    name = fields.Char(string='Appointment ID', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    patient_id = fields.Many2one(comodel_name='hospital.patient', string='Patient', required=True)
    doctor_ids = fields.One2many(comodel_name='hospital.doctor')
    patient_age = fields.Integer(string='Age', related='patient_id.age')
    note = fields.Text(string='Registration Note', default=_get_default_note, track_visibility='always')
    doctor_note = fields.Text(string="Doctor Note")
    pharmacy_note = fields.Text(string="Pharmacy Note")
    appointment_date = fields.Date(string='Date', required=True, default=datetime.today())
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, default='draft')


