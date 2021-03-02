from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError

# class ResPartners(models.Model):
#     _inherit = 'res.partner'
#
#     @api.model
#     def create(self, vals_list):
#         res = super(ResPartners, self).create(vals_list)
#         print("Yes, it worked")
#         # do the custome code here
#         return res

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _rec_name = "name"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    @api.constrains('age')
    def check_age(self):
        for patient in self:
            if patient.age <= 0:
                raise ValidationError(_('The age must be greater than 0'))

    @api.depends('age')
    def set_age_group(self):
        for patient in self:
            if patient.age < 18:
                patient.age_group = 'child'
            else:
                patient.age_group = 'adult'

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        result = super(HospitalPatient, self).create(vals)
        return result

    def open_patient_appointments(self):
        return {
            'name': _('Patient Appointments'),
            'view_mode': 'tree,form',
            'res_model': 'hospital.appointment',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.appointments.ids)],
        }

    def _compute_appointment_count(self):
        for patient in self:
            patient.appointment_count=len(patient.appointments)

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age')
    age_group = fields.Selection([
        ('adult', 'Adult'),
        ('child', 'Child'),
    ], string='Age Group', compute='set_age_group')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], required=True, default='male')
    note = fields.Text(string='Description', track_visibility='always')
    image = fields.Binary()
    name_seq = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    appointments = fields.One2many('hospital.appointment', 'patient_id', string='Appointments')
    doctor_rec = fields.One2many(related='appointments.doctor_id')

    appointment_count = fields.Integer(compute='_compute_appointment_count', help="The number of appointments related to this patient")


