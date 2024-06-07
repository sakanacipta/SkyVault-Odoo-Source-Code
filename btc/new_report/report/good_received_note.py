from odoo import api, models
import logging

_logger = logging.getLogger(__name__)


class GrnReport(models.AbstractModel):
    _name = "report.new_report.good_received_note"
    _description = "Good Received Note"

    @api.model
    def _get_report_values(self, docids, data=None):

        _logger.info(123)

        orders = []
        total_ordered = 0  # Initialize total product quantity
        total_received = 0  # Initialize total product quantity
        total_variance = 0  # Initialize total product quantity

        for id in docids:
            # Purchase Order table
            data = self.env["purchase.order"].search([("id", "=", id)])
            grn_date = data.effective_date
            po_no = data.name
            po_date = data.date_approve
            supplier_code = data.partner_id.id
            supplier_name = data.partner_id.name
            partner_ref = data.partner_ref
            driver_name = data.x_studio_driver_name
            driver_ic_no = data.x_studio_driver_ic_no
            vehicle_no = data.x_studio_vehicle_no

            # Stock Picking table
            stock_picking = self.env["stock.picking"].search(
                [("origin", "=", po_no), ("name", "like", "%/IN/%")]
            )
            grn_no = stock_picking.name

            # Purchase Order Line table
            products = self.env["purchase.order.line"].search(
                [("order_id", "=", po_no)]
            )

            # Initialize an empty list to store product data for each record
            product_data = []

            for product in products:
                product_info = {
                    "prod_code": product.name,
                    "prod_desc": product.name,
                    "uom": product.product_uom.name,
                    "qty_ordered": product.product_qty,
                    "qty_received": product.qty_received,
                    "variance_qty": product.variance_quantity,
                }
                product_data.append(product_info)

                # Add the quantity of the current product to the total quantity
                total_ordered += product.product_qty
                total_received += product.qty_received
                total_variance += product.variance_quantity

            data = {
                "grn_no": grn_no,
                "grn_date": grn_date,
                "supplier_code": supplier_code,
                "supplier_name": supplier_name,
                "partner_ref": partner_ref,
                "driver_name": driver_name,
                "driver_ic_no": driver_ic_no,
                "vehicle_no": vehicle_no,
                "po_no": po_no,
                "po_date": po_date,
                # table
                "products": product_data,
                # total product quantity
                "total_ordered": total_ordered,
                "total_received": total_received,
                "total_variance": total_variance,
            }

            orders.append(data)

        return {"orders": orders}
