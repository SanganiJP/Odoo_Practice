# -*- coding: utf-8 -*-
from odoo import models, fields, api


class HotelRoom(models.Model):
    _name = 'hotel.room'
    _description = 'Hotel Room'

    name = fields.Char(string="Room Number", required=True, copy=False)
    is_available = fields.Boolean(string="Is Available")
    category_id = fields.Many2one("hotel.room.category", string="Category")
    status = fields.Selection([('available', 'Available'),
                               ('booked', 'Booked')], default='available', string="Room Status")
