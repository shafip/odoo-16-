from odoo import models, fields, api

class VehicleAccessories(models.Model):
    _name = 'vehicle_accessories'
    _rec_name = 'customer_name'

    customer_name = fields.Many2one('res.partner', string='Customer Name')
    date = fields.Date(string='Date')
    vehicle_accessory_line_ids = fields.One2many('vehicle_accessory_line', 'vehicle_accessories_id', string='Vehicle Accessory Lines')
    grand_total = fields.Float(compute='_compute_grand_total', string='Grand Total')

    @api.depends('vehicle_accessory_line_ids.sub_total')
    def _compute_grand_total(self):
        for rec in self:
            rec.grand_total = sum(rec.vehicle_accessory_line_ids.mapped('sub_total'))

class VehicleAccessoryLine(models.Model):
    _name = 'vehicle_accessory_line'

    vehicle_accessories_id = fields.Many2one('vehicle_accessories', string='Vehicle Accessories')
    name = fields.Char(string='Name')
    type_of_vehicle_accessories = fields.Selection([('bike', 'Bike'), ('car', 'Car'), ('bus', 'Bus')], string='Type of vehicle accessories')
    code = fields.Char(string='Code')
    quantity = fields.Float(string='Quantity')
    price = fields.Float(string='Price')
    sub_total = fields.Float(string='Sub Total', compute='_compute_sub_total')

    @api.depends('price')
    def _compute_sub_total(self):
        for record in self:
            record.sub_total = record.price * record.quantity
