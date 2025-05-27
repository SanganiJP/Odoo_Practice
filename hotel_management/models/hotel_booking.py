# -*- coding: utf-8 -*-
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from odoo.exceptions import UserError


class HotelBooking(models.Model):
    _name = 'hotel.booking'
    _description = 'Hotel Booking'

    name = fields.Char(string="Booking No", default='New', copy=False, required=True,  index=True)
    partner_id = fields.Many2one("res.partner", string="Guest", required=True)
    email = fields.Char(string="Email ID", required=True)
    phone_no = fields.Char(string="Phone No", required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')], default='male', string="Gender", required=True)
    booking_date = fields.Date(string="Booking Date", default=date.today(), readonly=True)
    check_in_date = fields.Datetime(string="Check in date")
    check_out_date = fields.Datetime(string="Check out date")
    total_duration = fields.Float(string="Total Duration")
    number_of_guests = fields.Integer(string="Number of Guests")
    room_category = fields.Selection([('standard','Standard'), ('deluxe','Deluxe'), ('suite','Suite')], default='standard', string="Room Category", required=True )

    @api.model_create_multi
    def create(self, val_list):
        res = super(HotelBooking, self).create(val_list)
        for record in res:
            record.name = self.env["ir.sequence"].next_by_code('hotel.booking')
        return res

    @api.constrains('email_id')
    def validate_email(self):
        """ This method is ensure there is no guests with same email address. """
        for record in self:
            if record.email:
                email_ids = self.env['hotel.booking'].search_count([('email', '=', record.email)])
                if email_ids > 1:
                    raise UserError("Email ID already exists.")

    @api.constrains('phone_no')
    def validate_phone_no(self):
        """ This method is ensure there is no guest with same phone number. """
        for record in self:
            if record.phone_no:
                if not record.phone_no.isdigit():
                    raise UserError("Phone number must be in digits.")

                if len(record.phone_no) != 10:
                    raise UserError("Phone number should be 10 digits.")

                phone_numbers = self.env['hotel.booking'].search_count([('phone_no', '=', record.phone_no)])
                if phone_numbers > 1:
                    raise UserError("Phone no already exists.")

    @api.onchange('phone_no')
    def onchange_phone_no(self):
        if self.phone_no:
            if not self.phone_no.isdigit():
                raise UserError("Phone number must be in digits.")

    @api.onchange('check_in_date', 'total_duration')
    def onchange_check_out_date(self):
        """ This method give check out date on onchage check_in_date and total_duration. """
        if self.check_in_date:
            self.check_out_date = self.check_in_date + relativedelta(days=self.total_duration)
