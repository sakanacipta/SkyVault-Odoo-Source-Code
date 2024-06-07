from odoo import api, fields, models, _
from datetime import timedelta, datetime



class SaleOrder(models.Model):
    _inherit = 'sale.order'


    def storage_services_calculation(self):
        order_lines = []  # List to collect all order line data

        count_lines =  self.pricelist_id.stock_count_ids.filtered(lambda c: c.stock_lines)


        for line in count_lines.stock_lines:
            if line:
                    if line.location_id and line.location_id.product_ids:
                        for product in line.location_id.product_ids:
                            # Prepare each order line data
                            order_line_data = {
                                'product_id': product.id,
                                'product_uom_qty': line.quantity,
                                'order_id': self.id,
                                'services_charges': 'storage_services'
                            }
                            order_lines.append((0, 0, order_line_data))  # Append to the list

        if order_lines:
            # Update order_line field with all collected order line data
            self.write({'order_line': order_lines})
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    services_charges = fields.Selection([
        ('storage_services', 'Storage Services'),
        ('transfer_services', 'Transfer Services')], string='Services')






class ResPartner(models.Model):
    _inherit = 'res.partner'

    product_ids = fields.One2many('product.product', 'partner_id', string="products", check_company=True, )
    company_filters = fields.Boolean(related="company_id.filter", store=True)

    product_allocation_ids = fields.One2many('product.allocation', 'partner_id', string="Product Allocation")


class ProductProduct(models.Model):
    _inherit = 'product.product'

    partner_id = fields.Many2one("res.partner")
    company_filters = fields.Boolean(related="company_id.filter", store=True)


class StockPicking(models.Model):
    _inherit = 'stock.picking'



    def create_sale_order_from_pricelist(self):
        if self.state == "done" and self.company_id.filter:
            pricelist_intervals = {}

            # sale_orders = self.partner_id.property_product_pricelist.sale_ids
            sale_orders = sorted(self.partner_id.property_product_pricelist.sale_ids, key=lambda x: x.date_order)

            for i in range(len(sale_orders)):
                current_order = sale_orders[i]
                start_date = current_order.date_order
                next_order = sale_orders[i + 1] if i + 1 < len(sale_orders) else None

                if not next_order:
                    end_date = self.partner_id.property_product_pricelist.end_date
                else:
                    end_date = next_order.date_order

                if start_date <= self.scheduled_date <= end_date:
                    product_quantities = {}
                    for line in self.product_allocation_ids:
                        if line.product_id and line.quantity:
                            product_quantities[line.product_id.id] = line.quantity

                    order_lines = [(0, 0, {
                        'product_id': pid,
                        'product_uom_qty': qty,
                        'order_id': current_order.id,
                        'services_charges':'transfer_services',
                    }) for pid, qty in product_quantities.items()]
                    print(order_lines)

                    current_order.write({'order_line': order_lines})
        else:
            pass


class ProductAllocation(models.Model):
    _name = "product.allocation"

    product_id = fields.Many2one('product.product')
    partner_id = fields.Many2one('res.partner')
    company_filters = fields.Boolean(related="company_id.filter", store=True)
    company_id = fields.Many2one('res.company', required=True, readonly=True, default=lambda self: self.env.company)
    pricelist_id = fields.Many2one('product.pricelist')
    picking_ids = fields.Many2one('stock.picking', string="Picking")
    products_ids = fields.Many2many(related="picking_ids.products_ids", related_sudo=False)
    quantity = fields.Float(string='Quantity')

    @api.onchange('product_id')
    def product_onchange(self):
        for rec in self:
            if rec.product_id:
                rec.product_id.partner_id = rec.pricelist_id.partner_id.id
                rec.partner_id = rec.pricelist_id.partner_id.id

    @api.model
    def default_get(self, fields_list):
        defaults = super(ProductAllocation, self).default_get(fields_list)
        # Adjust the context key as needed based on how you're opening the allocation form/view
        pricelist_id = self.env.context.get('default_pricelist_id')
        if pricelist_id:
            pricelist = self.env['product.pricelist'].browse(pricelist_id)
            if pricelist.partner_id:
                defaults['partner_id'] = pricelist.partner_id.id
        return defaults

    @api.model
    def create(self, values):

        if 'product_id' in values and 'partner_id' in values:
            product = self.env['product.product'].browse(values['product_id'])
            product.sudo().write({'partner_id': values['partner_id']})
        return super(ProductAllocation, self).create(values)

    def write(self, values):
        result = super(ProductAllocation, self).write(values)

        if 'product_id' in values or 'partner_id' in values:
            for rec in self:
                if rec.product_id and rec.pricelist_id.partner_id:
                    rec.product_id.sudo().write({'partner_id': rec.partner_id.id})
        return result

    @api.model
    def unlink(self):
        for record in self:
            if record.product_id:
                record.product_id.sudo().write({'partner_id': False})
        return super(ProductAllocation, self).unlink()
