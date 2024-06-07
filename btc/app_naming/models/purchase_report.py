from odoo import api, fields, models

class SequenceMessageUpd(models.Model):
    _inherit = "purchase.report"
    _description = "Update purchase report state fields"

    state = fields.Selection([
        ('draft', 'Draft ASN'),
        ('sent', 'ASN Sent'),
        ('to approve', 'To Approve'),
        ('purchase', 'Check In Document'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], 'Status', readonly=True)