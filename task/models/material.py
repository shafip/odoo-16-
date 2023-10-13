from odoo import models, fields, api
from datetime import datetime, timedelta

class Material(models.Model):
    _name = 'material.master'
    _rec_name = 'customer_name'

    customer_name = fields.Many2one("res.partner", copy=False, string="Customer Name")
    collection_date = fields.Date(string='Collection Date', default=lambda self: (datetime.today() + timedelta(days=90)).date())
    material_list = fields.One2many('material.list', 'master_id', string='Material List')
    grand_total = fields.Float(compute='_compute_grand_total')
    current_user = fields.Many2one("res.users", default=lambda self: self.env.user, string="Current User")

    @api.depends('material_list.amount')
    def _compute_grand_total(self):
        for rec in self:
            rec.grand_total = sum(rec.material_list.mapped('amount'))

    def action_send_email(self):
        mail_template = self.env.ref('test_module.email_template')
        mail_template.send_mail(self.id,  force_send=True)
        print("success..........")

class MaterialList(models.Model):
    _name = 'material.list'

    master_id = fields.Many2one('material.master', string='Master')
    name = fields.Char(string='Name')
    quantity = fields.Integer(string='Quantity')
    code = fields.Char(string='Code')
    unit_price = fields.Float(string='Unit Price')
    amount = fields.Float(compute='_compute_amount', string='Amount')
    grand_total = fields.Float(compute='_compute_grand_total', string='Grand Total')

    @api.depends('quantity', 'unit_price')
    def _compute_amount(self):
        print("_compute_amount")
        for record in self:
            record.amount = record.quantity * record.unit_price

    @api.depends('amount')
    def _compute_grand_total(self):
        print('_compute_grand_total')
        grand_total = 0.0
        for record in self:
            print(record)
            grand_total += record.amount
        for record in self:
            record.grand_total = grand_total
        print(record.grand_total)
        return grand_total

