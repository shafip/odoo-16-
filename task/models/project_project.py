from odoo import models, fields, api

class InheritProject(models.Model):
    _inherit = 'project.project'

    sequence_number = fields.Char(string='Number', readonly=True)

    @api.model
    def create(self, vals_list):
        print('project sequence number')
        vals_list['sequence_number'] = self.env['ir.sequence'].next_by_code('project_sequence_number') or 'New'
        result = super(InheritProject, self).create(vals_list)
        return result
