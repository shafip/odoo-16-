from odoo import models, fields, api


class EmployeeInherits(models.Model):
    _inherit = "hr.employee"

    seq_number = fields.Char(string='Number', readonly=True)

    @api.model
    def create(self, vals_list):
        print('sequence_employee_number')
        vals_list['seq_number'] = self.env['ir.sequence'].next_by_code('sequence_employee_number') or 'New'
        result = super(EmployeeInherits, self).create(vals_list)
        return result

class EmployeeReview(models.Model):
    _name = 'employee.review'