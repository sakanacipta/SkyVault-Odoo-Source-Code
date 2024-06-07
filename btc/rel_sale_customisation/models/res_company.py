from odoo import api, fields, models, _


class Company(models.Model):
    _inherit = "res.company"

    filter = fields.Boolean(string="Product Filter" ,default=False, help="Active this field if you want to Product filteration based on customer associated to specific product ",)
