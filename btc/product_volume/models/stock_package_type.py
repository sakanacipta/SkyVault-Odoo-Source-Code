from odoo import api, models, fields


class PackageType(models.Model):
    _inherit = 'stock.package.type'

    lengths = fields.Char(string="Length", help="Enter length of the product")
    breadths = fields.Char(string="Width", help="Enter width of the product")
    heights = fields.Char(string="Height", help="Enter height of the product")
    length_uom = fields.Selection(
        selection=[('meters', 'Meters'), ('centimeters', 'Centimeters'),
                   ('inches', 'Inches'), ('feet', 'Feet'), ('yards', 'Yards')],
        string="UoM", default='meters', required=True,
        help="Select the unit of measure for length and")

    @api.onchange('lengths', 'breadths', 'heights')
    # remove condition
    def _onchange_product_measures(self):
        if self.lengths or self.breadths or self.heights:
            self.packaging_length = (float(self.lengths) * 1000)
            self.width = (float(self.breadths) * 1000)
            self.height = (float(self.heights) * 1000)

