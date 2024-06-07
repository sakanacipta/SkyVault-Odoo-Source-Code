# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    x_studio_driver_name = fields.Char(string="Driver Name")
    x_studio_driver_ic_no = fields.Char(string="Driver IC")
    x_studio_vehicle_no = fields.Char(string="Vehicle No")
    x_studio_receiver = fields.Many2one("res.partner", string="Receiver")

    def print_delivery_order(self):

        return self.env.ref("new_report.report_delivery_order").report_action(self)
