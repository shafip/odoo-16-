from odoo import models, fields, api


class SaleOrderInherits(models.Model):
    _inherit = 'sale.order.line'

    mrp = fields.Float(string='MRP', help="Product Mrp", related='product_template_id.mrp')
    image = fields.Binary(string='Image', related='product_template_id.image_1920')
    brand = fields.Char(related='product_template_id.brand')

    @api.depends("product_template_id")
    def action_history(self):
        print('action_history')
        domain = [
            "&",
            ("product_template_id", "=", self.product_id.name),
            ("order_partner_id", "=", self.order_id.partner_id.id),
        ]
        return {
            'action': 'product_template_new_price_button',
            "type": "ir.actions.act_window",
            "name": "Product History",
            "res_model": 'sale.order.line',
            "view_mode": "tree",
            "domain": domain,
            'target': 'new'
        }
