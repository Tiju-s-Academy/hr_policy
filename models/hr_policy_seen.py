
from odoo import fields,models

class HrPolicySeen(models.Model):
    _name = 'hr.policy.seen'
    _description = 'Seen Employees'

    policy_id = fields.Many2one('hr.policy', string="Policy", ondelete="cascade")
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    seen_time = fields.Datetime(string="Seen Time", default=fields.Datetime.now)
    seen = fields.Boolean(string='Seen',default=False)
