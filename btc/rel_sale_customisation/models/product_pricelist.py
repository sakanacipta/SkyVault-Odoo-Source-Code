from odoo import api, models, fields
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import timedelta, datetime


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        help='Select a customer to apply this pricelist.'
    )
    duration = fields.Selection([
        ('daily', 'Daily'),
        ('monthly', 'Monthly'),
        ('weekly', 'Weekly')], string="Invoice Frequency"
    )
    current_year = fields.Datetime.today().year
    is_leap_year = (current_year % 4 == 0 and (current_year % 100 != 0 or current_year % 400 == 0))
    days_in_year = 366 if is_leap_year else 365

    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")
    tenure = fields.Integer(string="Invoice Tenure", compute='_compute_tenure', store=True)
    item_list = fields.Many2many("product.product", string="Item list", )
    frequency_tenure = fields.Integer(string="Inventory Tenure", compute='_compute_tenure_frequency', store=True)



    inventory_duration = fields.Selection([
        ('daily', 'Daily'),
        ('monthly', 'Monthly'),
        ('weekly', 'Weekly')], string="Inventory Frequency"
    )

    product_allocation_ids = fields.One2many(related="partner_id.product_allocation_ids", string="Product Allocation",
                                             related_sudo=False)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], string='Status', default='draft')
    invoice_date = fields.Datetime(string="Next Invoice Date", compute='_compute_end_date')
    sale_ids = fields.One2many("sale.order", "pricelist_id", string="Sale orders")
    sale_count = fields.Integer(string="  Sale Order", compute='_compute_sale_count')
    stock_count_ids = fields.One2many('stock.count','pricelist_id','Inventory Counts')

    @api.depends('start_date', 'end_date', 'inventory_duration')
    def _compute_tenure_frequency(self):
        for record in self:
            if record.start_date and record.end_date:
                if record.end_date > record.start_date:
                    delta = relativedelta(record.end_date, record.start_date)
                    if record.inventory_duration == "daily":
                        record.frequency_tenure = (record.end_date - record.start_date).days
                    elif record.inventory_duration == "monthly":
                        # Approximation by converting years to months and adding the remaining months
                        record.frequency_tenure = delta.years * 12 + delta.months
                    elif record.inventory_duration == "weekly":
                        # Approximation by dividing the days by 7 to get the number of weeks
                        record.frequency_tenure = (record.end_date - record.start_date).days // 7
                else:
                    record.tenure = 0
                    return {
                        'warning': {
                            'title': "Validation Error",
                            'message': "End date must be greater than start date."
                        }
                    }

    def action_view_sales(self):
        action = self.env.ref('sale.action_orders').read()[0]
        action['domain'] = [('pricelist_id', '=', self.id)]
        action['context'] = {'default_pricelist_id': self.id}
        return action

    @api.depends('start_date', 'duration')
    def _compute_end_date(self):
        for pricelist in self:
            if pricelist.start_date and pricelist.duration == 'monthly':
                end_date = pricelist.start_date + relativedelta(months=1)
                end_datetime = datetime.combine(end_date, datetime.min.time()) + timedelta(hours=23, minutes=59)
                pricelist.invoice_date = end_datetime
            elif pricelist.start_date and pricelist.duration == 'weekly':
                end_date = pricelist.start_date + relativedelta(weeks=1)
                end_datetime = datetime.combine(end_date, datetime.min.time()) + timedelta(hours=23, minutes=59)
                pricelist.invoice_date = end_datetime
            # Add other conditions for different tenure options
            else:
                pricelist.invoice_date = False

    def confirm_and_create_sale_order(self):
        for pricelist in self:
            if pricelist.start_date and pricelist.end_date:
                list = []
                inventory = []
                for i in range(pricelist.tenure):
                    if pricelist.duration == 'monthly':
                        if list:
                            list.append(list[-1] + relativedelta(months=+1))
                        else:
                            list.append(pricelist.start_date)
                    elif pricelist.duration == 'weekly':
                        if list:
                            list.append(list[-1] + timedelta(days=7))
                        else:
                            list.append(pricelist.start_date)

                pricelist.write({'status': 'confirmed'})
                for date in list:
                    if date:
                        sale_order_values = {
                            'partner_id': pricelist.partner_id.id,
                            'date_order': date,
                        }
                        sale_order = self.env['sale.order'].create(sale_order_values)
                        print(sale_order)
                for i in range(pricelist.frequency_tenure):
                    if pricelist.inventory_duration == 'monthly':
                        if inventory:
                            inventory.append(inventory[-1] + relativedelta(months=+1))
                        else:
                            inventory.append(pricelist.start_date)
                    elif pricelist.inventory_duration == 'weekly':
                        if inventory:
                            inventory.append(inventory[-1] + timedelta(days=7))
                        else:
                            inventory.append(pricelist.start_date)
                for inv in inventory:
                    if inv:
                        inventory_count = {
                            'partner_id': pricelist.partner_id.id,
                            'date':inv,
                            'pricelist_id': pricelist.id
                        }
                        self.env['stock.count'].create(inventory_count)








    @api.depends('sale_ids')
    def _compute_sale_count(self):
        for pricelist in self:
            pricelist.sale_count = len(pricelist.sale_ids)

    def reset_to_draft(self):
        self.write({'status': 'draft'})

    @api.depends('start_date', 'end_date', 'duration')
    def _compute_tenure(self):
        for record in self:
            if record.start_date and record.end_date:
                if record.end_date > record.start_date:
                    delta = relativedelta(record.end_date, record.start_date)
                    if record.duration == "daily":
                        record.tenure = (record.end_date - record.start_date).days
                    elif record.duration == "monthly":
                        # Approximation by converting years to months and adding the remaining months
                        record.tenure = delta.years * 12 + delta.months
                    elif record.duration == "weekly":
                        # Approximation by dividing the days by 7 to get the number of weeks
                        record.tenure = (record.end_date - record.start_date).days // 7
                else:
                    record.tenure = 0
                    return {
                        'warning': {
                            'title': "Validation Error",
                            'message': "End date must be greater than start date."
                        }
                    }

    def create(self, vals):
        pricelist = super(ProductPricelist, self).create(vals)
        if pricelist.partner_id:
            pricelist.partner_id.property_product_pricelist = pricelist.id

        return pricelist

    # @api.onchange('start_date','end_date','item_ids')
    # def onchange_date(self):
    #     for pricelist in self:
    #         pricelist.item_ids.write({
    #             'date_start': pricelist.start_date,
    #             'date_end': pricelist.end_date,
    #         })

    def write(self, vals):
        res = super(ProductPricelist, self).write(vals)
        for record in self:
            if record.partner_id:
                record.partner_id.property_product_pricelist = record.id
        return res
