from odoo import api, models
import logging

_logger = logging.getLogger(__name__)


class UnloadingReport(models.AbstractModel):
    _name = "report.new_report.unloading"
    _description = "Unloading Report"

    @api.model
    def _get_report_values(self, docids, data=None):

        _logger.info(123)

        orders = []
        total_prod_qty = 0  # Initialize total product quantity

        for id in docids:
            # Stock Picking table
            data = self.env["stock.picking"].search([("id", "=", id)])
            name = data.name
            sender_name = data.partner_id.name
            sender_addr = data.partner_id.contact_address
            po_no = data.origin
            scheduled_date = data.scheduled_date
            status = data.state
            company_name = data.company_id.name

            # Stock Move Line table
            products = self.env["stock.move.line"].search([("picking_id", "=", name)])

            # Initialize an empty list to store product data for each record
            product_data = []

            for product in products:
                product_info = {
                    "prod_code": product.product_id.name,
                    "prod_desc": product.product_id.name,
                    "serial_no": product.lot_id.name,
                    "dest_loc": product.location_dest_id.name,
                    "uom": product.product_uom_id.name,
                    "qty": product.quantity,
                }
                product_data.append(product_info)

                # Add the quantity of the current product to the total quantity
                total_prod_qty += product.quantity

            data = {
                "grn_no": name,
                "scheduled_date": scheduled_date,
                "status": status,
                "sender_name": sender_name,
                "sender_addr": sender_addr,
                "po_no": po_no,
                "company_name": company_name,
                # table
                "products": product_data,
                # total product quantity
                "total_prod_qty": total_prod_qty,
            }

            orders.append(data)

        return {"orders": orders}
