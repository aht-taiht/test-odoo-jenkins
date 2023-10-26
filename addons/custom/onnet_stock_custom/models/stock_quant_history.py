from odoo import _, api, fields, models
from odoo.osv import expression

class StockQuantHistoty(models.Model):
    _name = 'stock.quant.history'

    def _domain_lot_id(self):
        domain = [
            "'|'",
                "('company_id', '=', company_id)",
                "('company_id', '=', False)"
        ]
        if self.env.context.get('active_model') == 'product.product':
            domain.insert(0, "('product_id', '=', %s)" % self.env.context.get('active_id'))
        elif self.env.context.get('active_model') == 'product.template':
            product_template = self.env['product.template'].browse(self.env.context.get('active_id'))
            if product_template.exists():
                domain.insert(0, "('product_id', 'in', %s)" % product_template.product_variant_ids.ids)
        else:
            domain.insert(0, "('product_id', '=', product_id)")
        return '[' + ', '.join(domain) + ']'

    parent_id = fields.Many2one('stock.quant.parent')
    quantity = fields.Float(compute='_compute_quantity', store=True)
    quantity = fields.Integer(
        'Quantity', readonly=True, store=True)
    lot_id = fields.Many2one(
        'stock.lot', 'Lot/Serial Number', index=True,
        ondelete='restrict', check_company=True,
        domain=lambda self: self._domain_lot_id())

    def _domain_product_id(self):
        domain = [('type', '=', 'product')]
        if self.env.context.get('product_tmpl_ids') or self.env.context.get('product_tmpl_id'):
            products = self.env.context.get('product_tmpl_ids', []) + [self.env.context.get('product_tmpl_id', 0)]
            domain = expression.AND([domain, [('product_tmpl_id', 'in', products)]])
        return domain

    product_id = fields.Many2one(
        'product.product', 'Product',
        domain=lambda self: self._domain_product_id(),
        ondelete='restrict', required=True, index=True, check_company=True)
    product_default_code = fields.Char(related='product_id.default_code', string='Mã nội bộ')
    barcode = fields.Char(related='product_id.barcode', store=True)
    product_tmpl_id = fields.Many2one(
        'product.template', string='Product Template',
        related='product_id.product_tmpl_id')
    product_categ_id = fields.Many2one(related='product_tmpl_id.categ_id')
    product_uom_id = fields.Many2one(
        'uom.uom', 'Unit of Measure',
        readonly=True, related='product_id.uom_id')
    priority = fields.Selection(related='product_tmpl_id.priority')
    company_id = fields.Many2one(related='location_id.company_id', string='Company', store=True, readonly=True)
    location_id = fields.Many2one(related='parent_id.location_id', store=True)
    storage_category_id = fields.Many2one(related='location_id.storage_category_id', store=True)
    cyclic_inventory_frequency = fields.Integer(related='location_id.cyclic_inventory_frequency', store=True)
    inventory_quantity = fields.Integer(
        'Counted Quantity', digits='Product Unit of Measure',
        help="The product's counted quantity.")
    inventory_diff_quantity = fields.Integer(
        'Difference', compute='_compute_inventory_diff_quantity', store=True,
        readonly=True, digits='Product Unit of Measure')
    inventory_quantity_set = fields.Boolean(store=True, compute='_compute_inventory_quantity_set', readonly=False,
                                            default=False)
    inventory_date = fields.Datetime('Ngày kiểm kê', default=fields.Datetime.now, store=True)
    write_uid = fields.Many2one(string='Người kiểm kê')

    @api.depends('inventory_quantity')
    def _compute_inventory_quantity_set(self):
        self.inventory_quantity_set = True

    @api.onchange('inventory_quantity')
    def _onchange_inventory_quantity(self):
        self.inventory_date = fields.Datetime.now()

    @api.depends('inventory_quantity')
    def _compute_inventory_diff_quantity(self):
        for quant in self:
            quant.inventory_diff_quantity = quant.inventory_quantity - quant.quantity

    @api.depends('product_id', 'location_id', 'lot_id')
    def _compute_quantity(self):
        for rec in self:
            rec.quantity = 0
            location_id = rec.location_id.id
            product_id = rec.product_id.id
            lot_id = rec.lot_id.id
            st_quant = self.env['stock.quant'].search([('location_id', '=', location_id), ('product_id', '=', product_id), ('lot_id', '=', lot_id)], limit=1)
            if st_quant:
                rec.quantity = st_quant.quantity