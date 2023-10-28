from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    delivery_id = fields.Many2one('delivery.type', string="Delivery Type")