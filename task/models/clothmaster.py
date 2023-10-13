from odoo import models, fields, api

class ClothesMaster(models.Model):
    _name = 'clothes.master'
    _description = 'Clothes Master'
    _rec_name = 'customer_name'

    customer_name = fields.Many2one('res.partner', string='Customer Name')
    date = fields.Date(string='Date')
    cloth_list_ids = fields.One2many('clothes.list', inverse_name='cloth_id', string='Cloth Line Ids')
    grand_total = fields.Float(compute='_compute_grand_total', string='Grand Total')

    @api.depends('cloth_list_ids.grand_total')
    def _compute_grand_total(self):
        print('_compute_grand_total')
        for rec in self:
            rec.grand_total = sum(rec.cloth_list_ids.mapped('grand_total'))

class ClothList(models.Model):
    _name = 'clothes.list'

    cloth_id = fields.Many2one('clothes.master', string='Cloth')
    cloth_name = fields.Char(string='Cloth Name', required=True)
    type_of_cloth = fields.Selection([('cotton', 'Cotton'), ('silk', 'Silk'), ('linen', 'Linen')], string='Type of Cloth')
    quantity = fields.Integer(string='Quantity')
    code = fields.Char(string='Code')
    amount = fields.Float(string='Amount')
    grand_total = fields.Float(compute='_compute_grand_total', string='Grand Total')

    @api.depends('amount')
    def _compute_grand_total(self):
        print('_compute_grand_total')
        for record in self:
            record.grand_total = record.amount * record.quantity