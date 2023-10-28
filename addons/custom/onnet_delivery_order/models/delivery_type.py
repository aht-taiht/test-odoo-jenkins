from odoo import models, fields


class DeliveryType(models.Model):
    _name = "delivery.type"

    name = fields.Char(string="Name")