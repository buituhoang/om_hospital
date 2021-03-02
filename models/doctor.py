from odoo import api, models, fields, _

from odoo.exceptions import UserError, ValidationError


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _description = "Hospital Doctor"
    _rec_name = "name"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    # _order = "id desc"

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.doctor.sequence') or _('New')
        result = super(HospitalDoctor, self).create(vals)
        return result

    name_seq = fields.Char(string='Doctor ID', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    name = fields.Char(string='Doctor Name', required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], required=True, default='male')
    user_id = fields.Many2one(comodel_name='res.users', string='Related User')
    appointment_id = fields.Many2one('hospital.appointment')

