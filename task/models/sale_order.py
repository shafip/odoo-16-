from odoo import models, fields, _, api
from odoo.exceptions import UserError


class SaleOrderInherits(models.Model):
    _inherit = 'sale.order'

    customer_order_lines = fields.One2many('sale.order.line', 'order_partner_id', string='Order Lines')
    CUSTOM_FIELD_STATES = {state: [('readonly', False)] for state in {'sale', 'cancel'}}
    date_order = fields.Datetime(string="Order Date", states=CUSTOM_FIELD_STATES, copy=False, required=True,
                                 default=None)

    def _prepare_confirmation_values(self):
        print(self.date_order)

        return {
            'state': 'sale',
        }

    def send_out_of_stock_notification(self):
        email_template = self.env.ref('task.product_stock_email_template')
        email_template.send_mail(self.id, force_send=True)
        print("success..........")

    def action_confirm(self):
        print('work it')
        """ Confirm the given quotation(s) and set their confirmation date.

        If the corresponding setting is enabled, also locks the Sale Order.

        :return: True
        :rtype: bool
        :raise: UserError if trying to confirm locked or cancelled SO's
        """
        for line in self.order_line:
            if line.product_id.qty_available < line.product_uom_qty:
                line.order_id.send_out_of_stock_notification()

        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                "It is not allowed to confirm an order in the following states: %s",
                ", ".join(self._get_forbidden_state_confirm()),
            ))

        self.order_line._validate_analytic_distribution()

        for order in self:
            order.validate_taxes_on_sales_order()
            if order.partner_id in order.message_partner_ids:
                continue
            order.message_subscribe([order.partner_id.id])

        self.write(self._prepare_confirmation_values())

        context = self._context.copy()
        context.pop('default_name', None)

        self.with_context(context)._action_confirm()
        if self.env.user.has_group('sale.group_auto_done_setting'):
            self.action_done()

        return True

    @api.model
    def create(self, vals):
        print('create')
        res = super(SaleOrderInherits, self).create(vals)
        for line in res.order_line:
            if line.product_id.type == 'product' and line.product_id.qty_available < line.product_uom_qty:
                purchase_order = self.env['purchase.order'].create({
                    'partner_id': line.order_partner_id.id,
                    'order_line': [(0, 0, {
                        'product_id': line.product_id.id,
                        'name': line.name,
                        'product_qty': line.product_uom_qty - line.product_id.qty_available,
                        'price_unit': line.product_id.standard_price,
                    })],
                    'state': 'draft',
                })
        return res


    # @api.model
    # def create(self, vals):
    #     print('create')
    #     res = super(SaleOrderInherits, self).create(vals)
    #     for line in res.order_line:
    #         if line.product_id.type == 'product' and line.product_id.qty_available < line.product_uom_qty:
    #             print(line.product_id.seller_ids.partner_id)
    #             purchase_order = self.env['purchase.order'].create({
    #                 'partner_id': line.product_id.seller_ids.partner_id[0].id or line.order_partner_id.id,
    #                 'order_line': [(0, 0, {
    #                     'product_id': line.product_id.id,
    #                     'name': line.name,
    #                     'product_qty': line.product_uom_qty - line.product_id.qty_available,
    #                     'price_unit': line.price_unit,
    #                 })],
    #                 'state': 'draft',
    #             })
    #     return res
