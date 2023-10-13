from odoo import models, api, fields

class AccountInvoice(models.Model):
    _inherit = 'account.move'

    @api.model
    def create(self, vals):
        print('invoice is work')
        invoice = super().create(vals)
        if invoice.amount_total > 0:
            payment = self.env['account.payment'].create({
                'partner_id': invoice.partner_id.id,
                'amount': invoice.amount_total,
                'name': self.move_type,
            })
        return invoice

class AccountInvoiceLine(models.Model):
    _inherit = 'account.move.line'

    product_brand = fields.Char(related='product_id.brand', string='Product Brand')
    mrp = fields.Float(related='product_id.mrp', string='Product Mrp')