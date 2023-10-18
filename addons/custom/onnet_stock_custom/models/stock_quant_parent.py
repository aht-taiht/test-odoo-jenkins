from odoo import api, fields, models, _

class StockQuant(models.Model):
    _name = 'stock.quant.parent'

    def _domain_location_id(self):
        if not self._is_inventory_mode():
            return
        return [('usage', 'in', ['internal', 'transit'])]

    @api.model
    def _is_inventory_mode(self):
        return self.env.context.get('inventory_mode') and self.user_has_groups('stock.group_stock_user')

    name = fields.Char()
    inventory_date = fields.Date(
        'Scheduled Date', compute='_compute_inventory_date', store=True, readonly=False,
        help="Next date the On Hand Quantity should be counted.")
    location_id = fields.Many2one(
        'stock.location', 'Location',
        domain=lambda self: self._domain_location_id(),
        auto_join=True, ondelete='restrict', required=True, index=True, check_company=True)
    quant_ids = fields.One2many('stock.quant', 'parent_id', copy=True, string='Quants')

    @api.depends('location_id')
    def _compute_inventory_date(self):
        quants = self.filtered(lambda q: not q.inventory_date and q.location_id.usage in ['internal', 'transit'])
        date_by_location = {loc: loc._get_next_inventory_date() for loc in quants.location_id}
        for quant in quants:
            quant.inventory_date = date_by_location[quant.location_id]