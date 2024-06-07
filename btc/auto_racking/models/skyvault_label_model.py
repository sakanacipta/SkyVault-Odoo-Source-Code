from odoo import fields, models, api
import qrcode
import base64
from io import BytesIO
import logging

_logger = logging.getLogger(__name__)

class SkyvaultPalletLabel(models.Model):
    _inherit = 'stock.picking'

    hide_label = fields.Boolean(compute='check_group')

    def create_stock_move_line(self,lot,new_lot_name):
        a = lot
        data = {
            "picking_id":a.picking_id.id,
            "move_id":a.move_id.id,
            "company_id":a.company_id.id,
            "product_id":a.product_id.id,
            "product_uom_id":a.product_uom_id.id,
            "location_id":a.location_id.id,
            "product_category_name":a.product_category_name,
            "lot_name":new_lot_name,
            "state":a.state,
            "reference":a.reference,
            "quantity":1,
            "quantity_product_uom":a.quantity_product_uom,
            "picked":a.picked
        }
        new_move_line = self.env['stock.move.line'].create(data)

    def update_lot_serial(self,lot_id,po_no,cust_do_no):
        counter = 0
        lot_arr = []
        #Count total formatted lot
        for a in lot_id:
            if a.lot_name:
                if po_no in a.lot_name:
                    lot_arr.append(a.lot_name)
                    counter += 1
        
        for a in lot_id:    
            lot_name = a.lot_name
            quantity = int(a.quantity)
            if not lot_name:
                for _ in range(quantity):
                    counter += 1
                    new_lot_name = po_no + "-" + cust_do_no + "-" + str(counter)
                    lot_arr.append(new_lot_name)
                    ##Create new lot
                    self.create_stock_move_line(a,new_lot_name)
                    ##Remove generic data
                a.unlink()
            elif po_no not in lot_name:
                for c in range(quantity):
                    counter += 1
                    new_lot_name = po_no + "-" + cust_do_no + "-" + lot_name + "-" + str(counter)
                    if c == 0:
                        a.write({
                            'lot_name': new_lot_name,
                            'quantity': 1
                        })
                    else:
                        ##Create new lot
                        self.create_stock_move_line(a,new_lot_name)
                    lot_arr.append(new_lot_name) 
            elif po_no in lot_name and quantity > 1:
                ##Update quantity to 1
                a.write({
                    'quantity': 1
                })
                ##Create new lot
                lot_name_sec = lot_name.split('-')
                for _ in range(quantity - 1):
                    counter += 1
                    if len(lot_name_sec) == 3:
                        new_lot_name = po_no + "-" + lot_name_sec[1] + "-" + str(counter)
                    else:
                        new_lot_name = po_no + "-" + lot_name_sec[1] + "-" + lot_name_sec[2] + "-" + str(counter)
                        ##Create new lot
                        self.create_stock_move_line(a,new_lot_name)
                    lot_arr.append(new_lot_name)
        return lot_arr

    def string_to_base64_qr(self,string_data):
        # Generate QR code image from the string
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(string_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Save QR code image to BytesIO buffer
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")

        # Encode image data to base64
        base64_encoded = base64.b64encode(buffer.getvalue()).decode('utf-8')

        buffer.close()

        return base64_encoded

    def check_group(self):
        data = self.read()[0]
        company_id = data['company_id'][0]
        picking_type = data['picking_type_id']
        picking_type_id = picking_type[0]
        picking_type_data = self.env['stock.picking.type'].search([(('id','=',picking_type_id))])
        sequence_code = picking_type_data['sequence_code']

        if sequence_code == "IN" and company_id == 1:
            self.hide_label = False
        else:
            self.hide_label = True

    def print_pallet_label(self):
        
        companies = self.env['res.company'].search([(('id','=','1'))])
        for company in companies:
            company_logo = company.logo.decode("utf-8")

        data = self.read()[0]
        # KLIA/IN/00015
        data_ref = data.get("name")

        # Get DO Number
        inbound = self.env['stock.picking'].search([(('name','=',data_ref))])
        for i in inbound:
            do = self.env['purchase.order'].search([(('name','=',i.origin))])
            po_no = do.name
            cust_do_no = do.partner_ref
            
            customer = i.partner_id
            cust_id = customer.id
            cust_name = customer.name
            cust_city = ""
            cust_zip = ""
            state_name = ""

            if customer.street2 is not None and bool(customer.street2):
                addr1 = customer.street + " " + customer.street2
            else:
                addr1 = customer.street
                
            state = customer.state_id
            if state.name is not None and bool(state.name):
                state_name = state.name

            if customer.city is not None and bool(customer.city):
                cust_city = customer.city
 
            if customer.zip is not None and bool(customer.zip):
                cust_zip = customer.zip

            if (cust_city != "" and cust_zip != ""):
                addr2 = cust_city + ", " + cust_zip + " " + state_name
            else:
                addr2 = state_name
        
        lot_id = self.env['stock.move.line'].search([(('reference','=',data_ref))])
        lots = self.update_lot_serial(lot_id,po_no,cust_do_no)

        lots_qr = []
        for lot in lots:
            lots_qr.append(self.string_to_base64_qr(lot))
                    
        data={
            'logo':company_logo,
            'po_no': po_no,
            'cust_id':cust_id,
            'cust_do_no':cust_do_no,
            'cust_name':cust_name,
            'ref_ids_arr':lots,
            'qrs':lots_qr,
            'addr1':addr1,
            'addr2':addr2,
            'form':self.read()[0]
        }

        return self.env.ref('auto_racking.action_label_skyvault').report_action(self,data=data)