# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class HotelBooking(models.Model):
    _name = 'hotel.booking'
    _description = 'Hotel Booking'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Booking No", default='New', copy=False, required=True, index=True)
    guest_id = fields.Many2one("hotel.guest", string="Guest", required=True)
    email = fields.Char(string="Email ID", required=True)
    phone_no = fields.Char(string="Phone No", required=True)
    booking_date = fields.Date(string="Booking Date", default=date.today(), readonly=True)
    check_in_date = fields.Date(string="Check in date", required=True)
    check_out_date = fields.Date(string="Check out date", readonly=True)
    total_duration = fields.Integer(string="Total Duration", default=1, required=True)
    number_of_guests = fields.Integer(string="Number of Guests", default=1, required=True)
    number_of_rooms = fields.Integer(string="Number of Rooms", default=1, required=True)
    category_id = fields.Many2one("hotel.room.category", string="Room Category", required=True)
    room_ids = fields.Many2many("hotel.room", string="Room Numbers")
    # room_id = fields.Many2one("hotel.room", string="Room Number")
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('cancel', 'Cancel')], string="state",
                             default="draft", tracking=True)
    total_amount = fields.Float(compute="_compute_total_amount", string="Total amount", store=True)
    price = fields.Float(string="Price", readonly=True)

    @api.model_create_multi
    def create(self, val_list):
        res = super(HotelBooking, self).create(val_list)
        for record in res:
            record.name = self.env["ir.sequence"].next_by_code('hotel.booking')
        return res

    @api.onchange('guest_id')
    def onchange_guest_id(self):
        self.email = self.guest_id.email
        self.phone_no = self.guest_id.phone_no

    @api.onchange('check_in_date', 'total_duration')
    def onchange_check_out_date(self):
        """ This method give check out date on onchage check_in_date and total_duration. """
        if self.check_in_date:
            self.check_out_date = self.check_in_date + relativedelta(days=self.total_duration)

    @api.onchange('check_in_date')
    def onchange_check_in_date(self):
        """ Onchange Date of birth it validate check in date. """
        if self.check_in_date:
            if self.check_in_date < date.today():
                raise UserError("Check in date must be future date!")

    def action_confirm(self):
        """ This method confirm room reservation. update room status to Reserved"""
        self.state = 'confirm'
        for room in self.room_ids:
            room_rec = self.env['hotel.room'].search([('id', '=', room.id)])
            if room_rec:
                room_rec.write({
                    'booking_ids': [(4, self.id)],
                    'is_available': False,
                    'status': 'reserved',
                })

        template_id = self.env.ref('hotel_management.room_booking_confirmation_mail_template')
        template_id.send_mail(self.id, force_send=True)

    def action_cancel(self):
        """ This method cancel the reservation"""
        self.state = 'cancel'
        for room in self.room_ids:
            room_rec = self.env['hotel.room'].search([('id', '=', room.id)])
            if room_rec:
                room_rec.write({
                    'is_available': True,
                    'status': 'available',
                })

    @api.onchange('category_id')
    def onchange_category_id(self):
        """ Onchange 'category_id', it set room price."""
        self.price = self.category_id.room_price

    @api.depends('price', 'number_of_rooms', 'total_duration')
    def _compute_total_amount(self):
        """ This method will compute total payment amount."""
        for rec in self:
            if rec.number_of_rooms and rec.total_duration and rec.price:
                rec.total_amount = rec.number_of_rooms * rec.total_duration * rec.price
            else:
                rec.total_amount = 0

    def get_generate_next_day_booking_data(self):
        """ return the previous day bookings detail"""
        bookings = self.env['hotel.booking'].search_count([
            ('booking_date', '=', date.today() - timedelta(days=1))
        ])
        return bookings

    def action_generate_next_day_booking_mail(self):
        """ Send next day's room reservation detail mail to admin. """
        template_id = self.env.ref('hotel_management.email_template_next_day_booking_mail')
        template_id.send_mail(self.id, force_send=True)