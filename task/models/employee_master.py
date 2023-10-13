from odoo import models, fields, api
from datetime import date

class Employees(models.Model):
    _name = 'employees.data'
    _rec_name = 'first_name'

    seq_number = fields.Char(string="Sequence Number")
    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Phone', required=True)
    department = fields.Many2one(string='Department', comodel_name='employee.department')
    hire_date = fields.Date(string='Hire Date')
    salary = fields.Float(string='Salary')
    reviewer_ids = fields.One2many('employee.review', inverse_name='employee_id')
    employee_note = fields.Text(string='Notes')

    @api.model
    def create(self, vals_list):
        print('employee sequence Number ')
        vals_list['seq_number'] = self.env['ir.sequence'].next_by_code('sequence_employee_number') or 'New'
        result = super(Employees, self).create(vals_list)
        return result

    def action_add_review(self):
        print('action_add_review')
        wizard = self.env['employee.wizard'].create({
            'employee_id': self.id
        })
        return {
            "type": "ir.actions.act_window",
            "name": "Employee Review",
            "res_model": "employee.wizard",
            "view_mode": "form",
            'target': 'new',
            'res_id': wizard.id,
        }
class Department(models.Model):
    _name = 'employee.department'

    name = fields.Char(string='Name', required=True)

class EmployeeReview(models.Model):
    _name = 'employee.review'

    employee_id = fields.Many2one('employees.data', string='Employee')
    reviewer = fields.Char(string='Reviewer')
    areas_for_improvement = fields.Text(string="Areas for Improvement")
    review_date = fields.Date('Review Date',  default=date.today(), invisible=True)
    performance_rating = fields.Selection([('week', 'Week'), ('average', 'Average'), ('good', 'Good'), ('excellent', 'Excellent')],
                                          string='Overall Performance Rating')

class InheritHrJob(models.Model):
    _inherit = 'hr.job'

    job_description = fields.Text(string="Job Description")

class EmployeeReviewWizard(models.TransientModel):
    _name = 'employee.wizard'

    employee_id = fields.Many2one('employees.data', string='Employee', readonly='True')
    reviewer = fields.Many2one('res.users', default=lambda self: self.env.user, string='Reviewer')
    areas_for_improvement = fields.Text(string="Areas for Improvement")
    review_date = fields.Date('Review Date', default=date.today(), invisible=True)
    performance_rating = fields.Selection(
        [('week', 'Week'), ('average', 'Average'), ('good', 'Good'), ('excellent', 'Excellent')],
        string='Overall Performance Rating')

    def action_review_create(self):
        print('action_add_review')
        review = self.env['employee.review'].create({
            'employee_id': self.employee_id.id,
            'reviewer': self.reviewer.name,
            'areas_for_improvement': self.areas_for_improvement,
            'review_date': self.review_date,
            'performance_rating': self.performance_rating
        })
