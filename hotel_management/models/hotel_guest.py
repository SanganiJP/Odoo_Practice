# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date


class HotelGuest(models.Model):
    _name = 'hotel.guest'
    _description = 'Hotel Guest'

    name = fields.Char(string="Name", required=True, copy=False)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')], default='male', string="Gender", required=True)
    email = fields.Char(string="Email ID", required=True)
    phone_no = fields.Char(string="Phone No", required=True)
    guest_type = fields.Selection([
        ('individual', 'Individual'),
        ('family', 'Family')], default='individual', string="Guest type", required=True)
    date_of_birth = fields.Date(string="Birth Date")
    age = fields.Integer(string="Age", readonly=True, required=True)
    booking_ids = fields.One2many("hotel.booking", "guest_id", string="Bookings")

    @api.onchange('date_of_birth')
    def onchange_date_of_birth(self):
        """ Onchange Date of birth it validate birthdate and count guest's age."""
        if self.date_of_birth:
            if self.date_of_birth > date.today():
                raise UserError("Birth date should be past date!")

            self.age = relativedelta(date.today(),self.date_of_birth).years
            # Calculate the difference between today's date and the guest's date of birth to get their age in years

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

