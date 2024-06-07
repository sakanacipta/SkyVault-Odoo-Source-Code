from odoo import api, models
import logging

_logger = logging.getLogger(__name__)


class UnloadingReport(models.AbstractModel):
    _name = "report.new_report.pick_list"
    _description = "Unloading Report"

    @api.model
    def _get_report_values(self, docids, data=None):

        _logger.info(123)

        orders = []

        for id in docids:
            # Stock Picking table
            data = self.env["stock.picking"].search([("id", "=", id)])
            name = data.name
            customer = data.partner_id.name
            do_no = data.origin
            date_done = data.date_done

            # Stock Move Line table
            products = self.env["stock.move.line"].search([("picking_id", "=", name)])

            # Initialize an empty list to store product data for each record
            product_data = []

            for product in products:
                product_info = {
                    "prod_code": product.product_id.name,
                    "prod_desc": product.product_id.name,
                    "source_loc": product.location_id.barcode,
                    "serial_no": product.lot_id.name,
                    "uom": product.product_uom_id.name,
                    "qty": product.quantity,
                }
                product_data.append(product_info)

            data = {
                "barcode_no": name,
                "date_done": date_done,
                "customer": customer,
                "do_no": do_no,
                # table
                "products": product_data,
            }

            orders.append(data)

        return {"orders": orders}
