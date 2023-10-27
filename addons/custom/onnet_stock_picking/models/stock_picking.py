from odoo import models, fields, api

class Picking(models.Model):
    _inherit = 'stock.picking'

    partner_address = fields.Char(string="Delivery Address", compute='_compute_address')
    delivery_id = fields.Many2one('delivery.type', string="Delivery Type", compute='_compute_delivery_type')

    # @api.depends('sale_id')
    def _compute_address(self):
        for picking in self:
            picking.partner_address = picking.sale_id.address if picking.sale_id else False

    @api.depends('sale_id', 'purchase_id')
    def _compute_delivery_type(self):
        for picking in self:
            if picking.sale_id and picking.sale_id.delivery_id:
                picking.delivery_id = picking.sale_id.delivery_id
            elif picking.purchase_id and picking.purchase_id.delivery_id:
                picking.delivery_id = picking.purchase_id.delivery_id
            else:
                picking.delivery_id = False
