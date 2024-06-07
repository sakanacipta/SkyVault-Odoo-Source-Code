# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class StockPutawayRule(models.Model):
    _inherit = 'stock.putaway.rule'

    cluster_id = fields.Many2one('stock.cluster')

class StockCluster(models.Model):
    _name = 'stock.cluster'
    _description = 'Cluster Configuration'
    _check_company_auto = True

    name = fields.Char()
    putaway_ids = fields.One2many('stock.putaway.rule', 'cluster_id')

    location_in_id = fields.Many2one(
        'stock.location', 'When product arrives in', check_company=True,
        domain="[('child_ids', '!=', False)]",
        required=True, ondelete='cascade', index=True)
    location_out_id = fields.Many2one(
        'stock.location', 'Store to sublocation', check_company=True,
        domain="[('id', 'child_of', location_in_id)]",
        required=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', required=True, ondelete='cascade', index=True)

    company_id = fields.Many2one(
        'res.company', 'Company', required=True,
        default=lambda s: s.env.company.id, index=True)

    @api.model_create_multi
    def create(self, vals_list):
        records = super(StockCluster, self).create(vals_list)
        for record in records:
            for product_id in record.partner_id.product_ids.ids:
                self.env['stock.putaway.rule'].create({
                    'cluster_id': record.id,
                    'location_in_id': record.location_in_id.id,
                    'product_id': product_id,
                    'location_out_id': record.location_out_id.id
                })
        return records

    def write(self, vals):
        res = super(StockCluster, self).write(vals)
        if vals.get('partner_id'):
            self.putaway_ids.unlink()
            for product_id in self.partner_id.product_ids.ids:
                self.env['stock.putaway.rule'].create({
                    'cluster_id': self.id,
                    'location_in_id': self.location_in_id.id,
                    'product_id': product_id,
                    'location_out_id': self.location_out_id.id
                })
        elif vals.get('location_in_id'):
            for putaway_id in self.putaway_ids:
                putaway_id.location_in_id = self.location_in_id.id
        elif vals.get('location_out_id'):
            for putaway_id in self.putaway_ids:
                putaway_id.location_out_id = self.location_out_id.id
        return res

    def unlink(self):
        self.putaway_ids.unlink()
        return super(StockCluster, self).unlink()
