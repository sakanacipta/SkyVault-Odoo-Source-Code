# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    x_studio_driver_name = fields.Char(string="Driver Name")
    x_studio_driver_ic_no = fields.Char(string="Driver IC")
    x_studio_vehicle_no = fields.Char(string="Vehicle No")

    def print_purchase_order(self):

        return self.env.ref("new_report.report_purchase_order").report_action(self)

    def print_good_received_note(self):

        return self.env.ref("new_report.report_grn").report_action(self)
