from odoo import models, fields

class ProductBrand(models.Model):
    _name = 'product.brand'

    name = fields.Char(string='Name', required=True)
