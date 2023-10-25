from odoo import models, fields, api

LOCKED_FIELD_STATES = {
    state: [('readonly', True)]
    for state in {'done', 'cancel'}
}


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    address = fields.Char(string="Delivery Address",
                          compute='_compute_address',
                          store=True, readonly=False, required=True, precompute=True,
                          states=LOCKED_FIELD_STATES,
                          domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", )

    @api.depends('partner_id')
    def _compute_address(self):
        for order in self:
            order.address = order.partner_id.contact_address_complete if order.partner_id else False
