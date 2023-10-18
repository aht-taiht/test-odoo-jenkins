from odoo import _, api, fields, models

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    parent_id = fields.Many2one('stock.quant.parent')
    location_id = fields.Many2one(compute='_compute_location_id', redonly=False)

    @api.depends('location_id', 'parent_id')
    def _compute_inventory_date(self):
        for rec in self:
            if rec.parent_id:
                rec.inventory_date = rec.parent_id.inventory_date
            else:
                super(StockQuant, self)._compute_inventory_date()

    @api.depends('parent_id')
    def _compute_location_id(self):
        for rec in self:
            rec.location_id = False
            if rec.parent_id:
                rec.location_id = rec.parent_id.location_id