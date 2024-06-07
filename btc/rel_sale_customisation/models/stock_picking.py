from odoo import api, models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    service_ids = fields.Many2many('product.product', string="Additional Services")
    products_ids =  fields.Many2many('product.product','rel_stock' ,string="Additional Services")
    company_filters = fields.Boolean(related="company_id.filter", store=True)


    # product_allocation_ids = fields.One2many('product.allocation','',)
    product_allocation_ids = fields.One2many('product.allocation','picking_ids',string="Services")


    def storage_services_count(self):
        current_date = fields.Date.today()
        allocations = self.env['product.allocation'].search([
            ('pricelist_id.validity_start', '<=', current_date),
            ('pricelist_id.validity_end', '>=', current_date),
            ('product_id.type', '=', 'service'),  # Filter for service products
        ])

        # Perform calculations based on the allocations found
        # For example, summing up the storage services for each allocation
        total_storage_services = sum(alloc.storage_service for alloc in allocations)






    @api.model
    def create(self, vals):
        record = super(StockPicking, self).create(vals)
        record.update_product_ids()
        return record

    def write(self, vals):
        result = super(StockPicking, self).write(vals)
        if 'partner_id' in vals:
            self.update_product_ids()
        return result
    @api.onchange('partner_id')
    def update_product_ids(self):
        for record in self:
            if record.partner_id and record.company_id.filter:
                product_ids = self.env['product.pricelist'].search([('partner_id', '=', record.partner_id.id)]).item_ids.mapped('product_id').ids
                record.products_ids = [(6, 0, product_ids)]



class StockLocation(models.Model):
    _inherit = "stock.location"

    category_id = fields.Many2one(
        'product.category',
        string='Service Category'
    )

    product_ids = fields.Many2many(
        'product.product',
        string='Services in Location',
        domain="[('categ_id', '=', category_id)]"
    )
