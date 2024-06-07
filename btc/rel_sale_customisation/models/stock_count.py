from odoo import api, fields, models, _
from datetime import date, datetime, time


class StockCount(models.Model):
    _name = "stock.count"
    _description = "Stock Count"

    partner_id = fields.Many2one("res.partner",'Partner')
    date = fields.Datetime('Inventry count date', default=lambda self: fields.Datetime.now())
    pricelist_id = fields.Many2one('product.pricelist',string="Pricelist")
    stock_lines = fields.One2many('stock.count.line','stock_count_id',"Stock Lines")



    def calculate_stock_(self):
        today_date = datetime.now()
        pricelists = self.env['product.pricelist'].search([('active', '=', True)])
        for pricelist in pricelists:
            count_dates = []
            for stock_count in pricelist.stock_count_ids:
                count_dates.append(stock_count.date)
            if count_dates:
                for i in range(len(count_dates)):
                    current_order = count_dates[i]
                    start_date = current_order
                    next_order = count_dates[i + 1] if i + 1 < len(count_dates) else None
                    if not next_order:
                        end_date = self.partner_id.property_product_pricelist.end_date
                    else:
                        end_date = next_order

                    if start_date <= today_date <= end_date:
                        product_with_qty_info = []
                        location = self.env['stock.location'].search([('usage', '=', 'internal')]).ids
                        for lec in location:
                            product_ids = self.env['product.product'].with_context(to_date=today_date,location=lec).search([('id','in',pricelist.product_allocation_ids.product_id.ids)])
                            for product in product_ids:
                                qty_available = product.qty_available
                                if qty_available == 0:
                                    continue
                                product_with_qty_info.append(
                                    {'product': product.id, 'qty': qty_available,'location':lec})
                        stock_count = self.env['stock.count'].search([('date','=',start_date),('pricelist_id','=',pricelist.id)])
                        if stock_count:
                            for info in product_with_qty_info:
                                stock_lines  = [(0, 0, {
                                    'product_id': info['product'],
                                    'quantity': info['qty'],
                                    'location_id':info['location'],
                                    'stock_count_id':stock_count.id,
                                    'date':today_date

                            })]
                                stock_count.write({'stock_lines':stock_lines})
                            pass












class StockCountline(models.Model):
    _name = "stock.count.line"
    _description = "Stock Count Line"


    stock_count_id = fields.Many2one('stock.count', string="Counts")
    date = fields.Datetime('Count date')
    product_id = fields.Many2one('product.product',string="product")
    location_id = fields.Many2one('stock.location',string="Location")
    quantity = fields.Integer("Quantity")



    








