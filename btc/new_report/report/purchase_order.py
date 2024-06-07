from odoo import api, models
import logging

_logger = logging.getLogger(__name__)


class PurchaseOrderReport(models.AbstractModel):
    _name = "report.new_report.purchase_order"
    _description = "Purchase Order"

    @api.model
    def _get_report_values(self, docids, data=None):

        orders = []
        total_prod_qty = 0  # Initialize total product quantity

        for id in docids:
            # Purchase Order table
            data = self.env["purchase.order"].search([("id", "=", id)])
            po_no = data.name
            po_date = data.date_approve
            delivery_date = data.effective_date
            partner_ref = data.partner_ref
            sender_name = data.partner_id.name
            sender_addr = data.partner_id.contact_address_complete
            sender_phone = data.partner_id.phone
            ship_to = data.company_id.name
            ship_to_addr = data.company_id.partner_id.contact_address_complete
            ship_to_phone = data.company_id.phone
            driver_name = data.x_studio_driver_name
            driver_ic_no = data.x_studio_driver_ic_no
            vehicle_no = data.x_studio_vehicle_no

            # Stock Picking table
            stock_picking = self.env["stock.picking"].search(
                [("origin", "=", po_no), ("name", "like", "%/IN/%")]
            )
            grn_no = stock_picking.name

            # Stock Move Line table
            products = self.env["stock.move.line"].search([("picking_id", "=", grn_no)])

            # Initialize an empty list to store product data for each record
            product_data = []

            for product in products:
                product_info = {
                    "prod_code": product.product_id.name,
                    "prod_desc": product.product_id.name,
                    "uom": product.product_uom_id.name,
                    "serial_no": product.lot_id.name,
                    "qty": product.quantity,
                }
                product_data.append(product_info)

                # Add the quantity of the current product to the total quantity
                total_prod_qty += product.quantity

            data = {
                "po_no": po_no,
                "po_date": po_date,
                "delivery_date": delivery_date,
                "partner_ref": partner_ref,
                "driver_name": driver_name,
                "driver_ic_no": driver_ic_no,
                "vehicle_no": vehicle_no,
                "sender_name": sender_name,
                "sender_addr": sender_addr,
                "sender_phone": sender_phone,
                "ship_to": ship_to,
                "ship_to_addr": ship_to_addr,
                "ship_to_phone": ship_to_phone,
                # table
                "products": product_data,
                # total product quantity
                "total_prod_qty": total_prod_qty,
            }

            orders.append(data)

        return {"orders": orders}
