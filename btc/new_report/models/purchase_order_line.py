# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    test_123 = fields.Char(string="Test 123")
    variance_quantity = fields.Float(
        string="Variance Quantity", compute="_compute_variance_quantity", store=True
    )

    @api.depends("product_qty", "qty_received")
    def _compute_variance_quantity(self):
        for line in self:
            line.variance_quantity = line.product_qty - line.qty_received
