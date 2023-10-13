from odoo import models, fields, api

class SchoolAccessories(models.Model):
    _name = 'school_accessories'
    _rec_name = 'customer_name'

    customer_name = fields.Many2one('res.partner', string='Customer Name')
    date = fields.Date(string='Date')
    school_accessory_line_ids = fields.One2many('school_accessory_line', 'school_accessories_id', string='School Accessory Lines')
    grand_total = fields.Float(compute='_compute_grand_total', string='Grand Total')

    @api.depends('school_accessory_line_ids.sub_total')
    def _compute_grand_total(self):
        for rec in self:
            rec.grand_total = sum(rec.school_accessory_line_ids.mapped('sub_total'))

class SchoolAccessoryLine(models.Model):
    _name = 'school_accessory_line'


    school_accessories_id = fields.Many2one('school_accessories', string='School Accessories')
    name = fields.Char(string='Name')
    code = fields.Char()
    quantity = fields.Float(string='Quantity')
    price = fields.Float(string='Price')
    sub_total = fields.Float(string='Sub Total', compute='_compute_sub_total')

    @api.depends('price')
    def _compute_sub_total(self):
        for record in self:
            record.sub_total = record.price * record.quantity
