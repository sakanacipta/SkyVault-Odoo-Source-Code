# -*- coding: utf-8 -*-

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def print_pick_list(self):

        return self.env.ref("new_report.report_pick_list").report_action(self)

    def print_unloading(self):

        return self.env.ref("new_report.report_unloading").report_action(self)

    def print_putaway(self):

        return self.env.ref("new_report.report_putaway").report_action(self)
