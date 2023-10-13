from odoo import models, fields, api
from odoo.exceptions import ValidationError


class InProductMrp(models.Model):
    _inherit = 'product.template'

    mrp = fields.Float(string='MRP', help="Product Mrp", required=True)
    seq_number = fields.Char(string='Number', readonly=True)
    brand_id = fields.Many2one('product.brand', string='Product Brand')
    brand = fields.Char(related='brand_id.name', string='Brand')

    @api.constrains('list_price', 'mrp')
    def _check_sale_price(self):
        for record in self:
            if record.list_price > record.mrp:
                raise ValidationError(f"Sale Price Not Grete than MRP : {record.mrp}")

    @api.model
    def create(self, vals_list):
        print('product sequence Number ')
        vals_list['seq_number'] = self.env['ir.sequence'].next_by_code('product_sequence_number') or 'New'
        result = super(InProductMrp, self).create(vals_list)
        return result

    def action_update_price(self):
        print('action_update_price')
        wizard = self.env['update.price.wizard'].create({
            'product_id': self.id
        })
        return {
            'action': 'product_template_new_price_button',
            'name': 'new price product',
            'type': 'ir.actions.act_window',
            'res_model': 'update.price.wizard',
            'view_mode': 'form',
            'res_id': wizard.id,
            'target': 'new'
        }

class ProductPriceWizard(models.TransientModel):
    _name = 'update.price.wizard'

    new_price = fields.Float(string='New Price', store=True)
    product_id = fields.Many2one("product.template")

    def update_list_price(self):
        print('update_list_price')
        self.product_id.list_price = self.new_price
        return {'type': 'ir.actions.act_window_close'}


class ProductSupplierInfoInherit(models.Model):
    _inherit = 'product.supplierinfo'

    partner_id = fields.Many2one(
        'res.partner', 'Vendor', ondelete='cascade', required=True, check_company=True,
        domain=lambda self: self._get_partner_domain()
    )

    def _get_partner_domain(self):
        domain = []
        state = 'approved'
        domain.append(('vendor_state', '=', state))
        return domain



