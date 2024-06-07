from odoo import api, models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    partner_product_ids = fields.One2many(related='partner_id.product_ids',
                                          string="Partner product", related_sudo=False, check_company=True, )
    company_filters = fields.Boolean(related="company_id.filter", store=True)

    pricelist_product = fields.Many2many(related="partner_id.property_product_pricelist.item_list", related_sudo=False )
    product_ids_domain = fields.Many2many('product.product', compute='_compute_product_ids_domain', store=False)


    # product_storable_ids = fields.One2many(related='partner_id.property_product_pricelist.product_allocation_ids',related_sudo=False )

    @api.depends('partner_id.property_product_pricelist', 'company_id.filter')
    def _compute_product_ids_domain(self):
        for record in self:
            # Clear the domain if the company setting is not to apply
            if not record.company_id.filter:
                allocated_products = self.env['product.product'].search([('type', '=', 'product')]).ids
                record.product_ids_domain = [(6, 0, allocated_products)]
            else:
                # Apply the domain only if the company setting is true
                if record.partner_id.property_product_pricelist:
                    allocated_products = record.partner_id.property_product_pricelist.product_allocation_ids.mapped('product_id.id')
                    record.product_ids_domain = [(6, 0, allocated_products)]
                else:
                    record.product_ids_domain = [(6, 0, [])]