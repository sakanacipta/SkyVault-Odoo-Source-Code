from odoo import api, fields, models

class InheritedModel(models.Model):
    _inherit = "purchase.order"
    _description = "Update purchase order state fields"

    state = fields.Selection([
        ('draft', 'ASN'),
        ('sent', 'ASN Sent'),
        ('to approve', 'To Approve'),
        ('purchase', 'Check In Document'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)
