from odoo import models, fields, api


class ResPartnerInherits(models.Model):
    _inherit = "res.partner"

    seq_number = fields.Char(string='Number', readonly=True)
    vendor_state = fields.Selection([('approved', 'Approved'), ('waiting', 'Waiting')], string='State')
    clothes_ids = fields.One2many("clothes.master", "customer_name", string="Clothes")
    count_clothes = fields.Integer(compute='_compute_cloth_count', string='Count Clothes')
    vehicle_accessories_ids = fields.One2many("vehicle_accessories", "customer_name", string="Vehicle")
    count_vehicle = fields.Integer(compute='_compute_vehicle_count', string='Count Vehicle')
    school_accessories_ids = fields.One2many("school_accessories", "customer_name", string="School")
    count_school_accessories = fields.Integer(compute='_compute_school_count', string='Count School Accessories')
    food_items_ids = fields.One2many("food.items", "customer_name", string="Food Items")
    count_food_items = fields.Integer(compute='_compute_food_count', string='Count Food Items')
    material_ids = fields.One2many("material.master", "customer_name", string="Material")
    count_material = fields.Integer(compute="_compute_material_count", string='Count Material')

    @api.model
    def create(self, vals_list):
        if vals_list.get('supplier_rank') == 1:
            vals_list['seq_number'] = self.env['ir.sequence'].next_by_code('vendor_sequence_number')
        elif vals_list.get('customer_rank') == 1:
            vals_list['seq_number'] = self.env['ir.sequence'].next_by_code('customer_sequence_number')
        result = super(ResPartnerInherits, self).create(vals_list)
        return result

    @api.depends("clothes_ids")
    def _compute_cloth_count(self):
        for record in self:
            record.count_clothes = len(record.clothes_ids)
        print(self.count_clothes)

    @api.depends("vehicle_accessories_ids")
    def _compute_vehicle_count(self):
        print('count vehicle')
        for record in self:
            record.count_vehicle = len(record.vehicle_accessories_ids)

    @api.depends("school_accessories_ids")
    def _compute_school_count(self):
        print('count school')
        for record in self:
            record.count_school_accessories = len(record.school_accessories_ids)

    @api.depends("food_items_ids")
    def _compute_food_count(self):
        print('count school')
        for record in self:
            record.count_food_items = len(record.food_items_ids)

    @api.depends("material_ids")
    def _compute_material_count(self):
        for record in self:
            record.count_material = len(record.material_ids)

    @api.depends("clothes_ids")
    def stat_clothes_view_action(self):
        print('work stat button')
        return {
            "type": "ir.actions.act_window",
            "name": "Clothes",
            "res_model": "clothes.master",
            "view_mode": "tree",
            "domain": [("customer_name", "=", self.ids)],
            'target': 'new',
        }

    @api.depends("vehicle_accessories_ids")
    def stat_vehicle_accessories_view_action(self):
        print('stat_vehicle_accessories_view_action')
        return {
            "type": "ir.actions.act_window",
            "name": "vehicle accessories",
            "res_model": "vehicle_accessories",
            "view_mode": "tree",
            "domain": [("customer_name", "=", self.ids)],
            'target': 'new',
        }

    @api.depends("school_accessories_ids")
    def stat_school_accessories_view_action(self):
        print('stat_school_accessories_view_action')
        return {
            "type": "ir.actions.act_window",
            "name": "school accessories",
            "res_model": "school_accessories",
            "view_mode": "tree",
            "domain": [("customer_name", "=", self.ids)],
            'target': 'new',
        }

    @api.depends("food_items_ids")
    def stat_food_items_view_action(self):
        print('food_items_ids')
        return {
            "type": "ir.actions.act_window",
            "name": "Food Items",
            "res_model": "food.items",
            "view_mode": "tree",
            "domain": [("customer_name", "=", self.ids)],
            'target': 'new',
        }

    @api.depends("material_ids")
    def stat_material_action(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Material",
            "res_model": "material.master",
            "view_mode": "tree",
            "domain": [("customer_name", "=", self.ids)],
            'target': 'new',
        }
