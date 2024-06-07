from odoo import api, models
import logging

_logger = logging.getLogger(__name__)


class DeliveryOrderReport(models.AbstractModel):
    _name = "report.new_report.delivery_order"
    _description = "Delivery Order"

    @api.model
    def _get_report_values(self, docids, data=None):

        orders = []
        total_prod_qty = 0  # Initialize total product quantity

        for id in docids:
            # Sale Order table
            data = self.env["sale.order"].search([("id", "=", id)])
            do_no = data.name
            do_date = data.date_order
            delivery_date = data.effective_date
            source_doc = data.origin
            send_from = data.company_id.name
            send_from_addr = data.company_id.partner_id.contact_address_complete
            send_from_phone = data.company_id.phone
            bill_to = data.partner_id.name
            bill_to_addr = data.partner_id.contact_address_complete
            bill_to_phone = data.partner_id.phone
            ship_to = data.x_studio_receiver.name
            ship_to_addr = data.x_studio_receiver.contact_address_complete
            ship_to_phone = data.x_studio_receiver.phone

            # Stock Picking table
            stock_picking = self.env["stock.picking"].search(
                [("origin", "=", do_no), ("name", "like", "%OUT%")]
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
                "do_no": do_no,
                "do_date": do_date,
                "delivery_date": delivery_date,
                "source_doc": source_doc,
                "send_from": send_from,
                "send_from_addr": send_from_addr,
                "send_from_phone": send_from_phone,
                "bill_to": bill_to,
                "bill_to_addr": bill_to_addr,
                "bill_to_phone": bill_to_phone,
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
