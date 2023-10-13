from odoo import models, fields


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    mrp = fields.Float(string='MRP', help="Product Mrp", related='product_id.product_tmpl_id.mrp')
    image = fields.Binary(string='ProductImage', related="product_id.image_1920")
    product_brand = fields.Many2one(related='product_id.brand_id',  string='Product Brand')
