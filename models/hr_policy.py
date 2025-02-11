from odoo import fields, models, api, _


class HrPolicy(models.Model):
    _name = 'hr.policy'
    _description = 'HR Policy'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'title'

    responsible_id = fields.Many2one('hr.employee', string='Responsible HR', default=lambda self: self.env.user.employee_id,
                                     required=True)
    tag_ids = fields.Many2many('policy.tags', string='Tags')
    title = fields.Char(string='Title')
    attachment = fields.Binary()
    summary = fields.Html()
    date = fields.Datetime(string='Published On | Updated On')
    state = fields.Selection([('draft', 'Draft'), ('published', 'Published')], string='Status', tracking=True,
                             default='draft')
    seen_by_data = fields.One2many('hr.policy.seen', 'policy_id', string="Seen By")
    type_of_file = fields.Selection([('pdf', 'PDF'), ('write', 'Write')], string='Type', default='pdf')
    status = fields.Boolean(string='status', compute='_compute_status')

    has_seen = fields.Boolean(string="Has Seen", compute="_compute_has_seen", store=False)

    @api.depends('seen_by_data')
    def _compute_has_seen(self):
        """ Check if the logged-in employee has seen the policy """
        current_employee = self.env.user.employee_id
        for record in self:
            record.has_seen = any(seen.employee_id == current_employee for seen in record.seen_by_data)



    def action_publish(self):
        self.write({
            'date': fields.Datetime.now(),
            'state': 'published'
        })
        active_employees = self.env['hr.employee'].search([('active', '=', True)])
        print("Active employee", active_employees)
        for employee in active_employees:
            print("send")
            self.activity_schedule(
                'hr_policy.mail_activity_hr_policy',
                summary = _('A new HR policy has been published. Please review it'),
                user_id = employee.user_id.id
            )

    def action_seen(self):
        """Mark the policy as seen when a user clicks 'View'"""
        current_employee = self.env.user.employee_id
        existing_record = self.seen_by_data.filtered(lambda r: r.employee_id == current_employee)
        if self.attachment:
            if not existing_record:
                self.seen_by_data = [(0, 0, {
                    'employee_id': current_employee.id,
                    'seen_time': fields.Datetime.now(),
                    'seen': True,
                })]
                activity_ids = self.activity_ids
                if activity_ids:
                    activity_ids.unlink()

    def action_update_policy(self):

        for record in self:
            record.state = 'draft'
            record.seen_by_data.unlink()
            record.activity_ids.unlink()

class PolicyTag(models.Model):
    _name = 'policy.tags'

    name = fields.Char(string='Name')
    color = fields.Integer(string='Color')