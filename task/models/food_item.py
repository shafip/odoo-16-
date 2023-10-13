from odoo import models, fields, api


class FoodItems(models.Model):
    _name = 'food.items'
    _rec_name = 'customer_name'


    customer_name = fields.Many2one('res.partner', string='Customer Name')
    date = fields.Date(string='Date')
    food_item_line_ids = fields.One2many('food.item.line', 'food_item_id', string='Food List')
    grand_total = fields.Float(string='Grand Total', compute='_compute_grand_total')

    @api.depends('food_item_line_ids.sub_total')
    def _compute_grand_total(self):
        for rec in self:
            rec.grand_total = sum(rec.food_item_line_ids.mapped('sub_total'))


class FoodItemline(models.Model):
    _name = 'food.item.line'

    food_item_id = fields.Many2one('food.items', string='Food Items')
    name = fields.Char(string='Name')
    code = fields.Char()
    quantity = fields.Float(string='Quantity')
    price = fields.Float(string='Price')
    sub_total = fields.Float(string='Sub Total', compute='_compute_sub_total')

    @api.depends('price')
    def _compute_sub_total(self):
        for record in self:
            record.sub_total = record.price * record.quantity