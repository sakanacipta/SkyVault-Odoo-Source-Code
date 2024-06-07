# -*- coding: utf-8 -*-

from odoo import models, fields, api

class my_module(models.Model):
    _name = 'auto_racking.location'
    _description = 'Auto Racking'

    pallet_id = fields.Text()
    location = fields.Text()
    reference = fields.Text()