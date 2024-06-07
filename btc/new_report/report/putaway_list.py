from odoo import api, models
import logging

_logger = logging.getLogger(__name__)


class PutawayReport(models.AbstractModel):
    _name = "report.new_report.putaway_list"
    _description = "Putaway List Report"

    @api.model
    def _get_report_values(self, docids, data=None):

        orders = []

        for id in docids:
            # Stock Picking table
            data = self.env["stock.picking"].search([("id", "=", id)])
            name = data.name
            effective_date = data.date_done

            # Stock Move Line table
            products = self.env["stock.move.line"].search([("picking_id", "=", name)])

            # Initialize an empty list to store product data for each record
            product_data = []

            for product in products:
                product_info = {
                    "prod_code": product.product_id.name,
                    "dest_loc": product.location_dest_id.name,
                    "uom": product.product_uom_id.name,
                    "qty": product.quantity,
                }
                product_data.append(product_info)

            data = {
                "grn_no": name,
                "effective_date": effective_date,
                # table
                "products": product_data,
            }

            orders.append(data)

        return {"orders": orders}
