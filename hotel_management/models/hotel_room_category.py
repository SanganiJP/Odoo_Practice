# -*- coding: utf-8 -*-
from odoo import models, fields, api


class HotelRoomCategory(models.Model):
    _name = 'hotel.room.category'
    _description = 'Hotel Room Category'

    name = fields.Char(string="Category", copy=False)
    number_of_beds = fields.Integer(string="Number of Beds")
    has_ac = fields.Boolean(string="Has AC")
    room_price = fields.Float(string="Room Price")
    # room_type = fields.Selection([('standard','Standard'), ('deluxe','Deluxe'), ('suite','Suite')], default='standard', string="Room Type", required=True)
    # booking_id = fields.Many2one()