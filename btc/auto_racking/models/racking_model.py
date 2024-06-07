from odoo import fields, models
import logging

_logger = logging.getLogger(__name__)

class RackingPDFReport(models.Model):
    _inherit = 'stock.picking'

    def print_racking_pdf(self):
        data={
            'model':'stock.picking',
            'form':self.read()[0]
        }

        return self.env.ref('auto_racking.action_report_auto_racking').report_action(self,data=data)      