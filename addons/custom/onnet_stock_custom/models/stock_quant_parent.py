from odoo import api, fields, models, _
from ast import literal_eval

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
    inventory_date = fields.Date('Ngày kiểm kê', default=fields.Date.today, store=True, readonly=False)
    location_id = fields.Many2one(
        'stock.location', 'Location',
        domain=lambda self: self._domain_location_id(),
        auto_join=True, ondelete='restrict', required=True, index=True, check_company=True)
    quant_ids = fields.One2many('stock.quant.history', 'parent_id', copy=True, string='Quants')

    def action_to_take_inventory(self):
        if not self.quant_ids:
            st_quants = self.env['stock.quant'].search([('location_id', '=', self.location_id.id)])
            data_quants = []
            for st_quant in st_quants:
                data_quants.append({
                    'product_id': st_quant.product_id.id,
                    'location_id': st_quant.location_id.id,
                    'quantity': st_quant.quantity,
                    'lot_id': st_quant.lot_id.id,
                    'parent_id': self.id
                })
            self.env['stock.quant.history'].create(data_quants)
        return {
            'name': _('Quants'),
            'res_model': 'stock.quant.history',
            'view_mode': 'tree',
            'views': [
                (self.env.ref('onnet_stock_custom.view_quant_history_tree').id, 'tree'),
            ],
            'type': 'ir.actions.act_window',
            'domain': [('parent_id', '=', self.id)],
            'context': {'default_parent_id': self.id}
        }
