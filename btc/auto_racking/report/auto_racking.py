from odoo import api,models
import logging

_logger = logging.getLogger(__name__)

class AutoRackingReport(models.AbstractModel):
    _name = 'report.auto_racking.auto_racking_template_2'
    _description = "Auto Racking Report"

    @api.model
    def _get_report_values(self,docids,data=None):
        if not self.env.context.get('active_model') or not self.env.context.get('active_id'):
            raise UserError(("Form content is missing, this reort cannot be printed."))
        
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))

        loc_list = []
        docs_list = []

        for id in docids:
            doc_details = self.env['stock.picking'].search([('id', '=', id)])
            doc_name = doc_details.name
            docs_list.append(doc_name)
            auto_rack_loc = self.env['auto_racking.location'].search([('reference','=',doc_details.name)])
            for loc in auto_rack_loc:
                vals = {
                    'pallet_id': loc.pallet_id,
                    'location_id': loc.location,
                    'reference': loc.reference
                }
                loc_list.append(vals)
        
        return {
            'doc_ids': docids,
            'doc_model': model,
            'data': data,
            'docs': docs,
            'locs': loc_list,
            'docs_list': docs_list
        }


