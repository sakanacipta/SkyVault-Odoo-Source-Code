from odoo import api, models, fields


class ProductDimensionsVolume(models.Model):
    _inherit = 'product.template'

    length = fields.Char(string="Length", help="Enter length of the product")
    breadth = fields.Char(string="Breadth", help="Enter breadth of the product")
    height = fields.Char(string="Height", help="Enter height of the product")

    # length_uom = fields.Selection(
    #     selection=[('meters', 'Meters'), ('centimeters', 'Centimeters'),
    #                ('inches', 'Inches'), ('feet', 'Feet'), ('yards', 'Yards')],
    #     string="UoM", default='meters', required=True,
    #     help="Select the unit of measure for length and")
    # volume_uom = fields.Selection(
    #     selection=[('cubic_meters', 'Cubic Meters'),
    #                ('cubic_inches', 'Cubic Inches'),
    #                ('cubic_feet', 'Cubic Feet'),
    #                ('cubic_yards', 'Cubic Yards')],
    #     string="UoM of Volume", default='cubic_meters', required=True,
    #     help="Select the unit of measure for volume")

    @api.onchange('length', 'breadth', 'height')
    def _onchange_product_measures(self):
        volume = (float(self.length if self.length else 0) *
                  float(self.breadth if self.breadth else 0) * float(
                    self.height if self.height else 0))
        self.volume = volume
