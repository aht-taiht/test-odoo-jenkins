from odoo import models, fields, api

class Picking(models.Model):
    _inherit = 'stock.picking'

    partner_address = fields.Char(string="Delivery Address", compute='_compute_address')

    # @api.depends('sale_id')
    def _compute_address(self):
        for picking in self:
            picking.partner_address = picking.sale_id.address if picking.sale_id else False
