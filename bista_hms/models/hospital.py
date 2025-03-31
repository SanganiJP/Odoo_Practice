from odoo import models, fields, api

class ResHospital(models.Model):
    _name = "hospital.hospital"
    _description = "hospital model"

    name = fields.Char(string="Name",required=True)
    hospital_ids = fields.One2many("res.doctor","hospital_id",string="Hospital Data")

    # from datetime import datetime
    # from dateutil.relativedelta import relativedelta
    #
    # date1 = datetime(2020, 1, 15)
    # date2 = datetime(2023, 4, 10)
    #
    # # Total days
    # total_days = (date2 - date1).days
    #
    # # Exact years, months, and days
    # difference = relativedelta(date2, date1)
    #
    # print(f"Total Years: {(date2.year - date1.year)}")
    # print(f"Total Months: {(date2.year - date1.year) * 12 + (date2.month - date1.month)}")
    # print(f"Total Days: {total_days}")
    # print(f"Exact Difference: {difference.years} years, {difference.months} months, {difference.days} days")

    # Current date and time
    # now = datetime.now()

    # Convert to string with custom format
    # date_str = now.strftime("%Y-%m-%d %H:%M:%S")
    # print("Formatted DateTime:", date_str)

    # Given dates in string format
    # date_str1 = "2020-01-15"
    # date_str2 = "2023-04-10"
    #
    # # Convert string to datetime object
    # date1 = datetime.strptime(date_str1, "%Y-%m-%d")
    # date2 = datetime.strptime(date_str2, "%Y-%m-%d")
    #
    # # Total days
    # total_days = (date2 - date1).days
    #
    # # Exact years, months, and days
    # difference = relativedelta(date2, date1)
    #
    # # Total months
    # total_months = (date2.year - date1.year) * 12 + (date2.month - date1.month)
    #
    # # Print results
    # print(f"Total Years: {date2.year - date1.year}")
    # print(f"Total Months: {total_months}")
    # print(f"Total Days: {total_days}")
    # print(f"Exact Difference: {difference.years} years, {difference.months} months, {difference.days} days")

    # # Get all sale orders
    # sale_orders = self.env['sale.order'].search([])
    #
    # # Filter orders where state is 'draft' and then delete them
    # sale_orders.filtered(lambda order: order.state == 'draft').unlink()

    # # Get all sale order lines
    # order_lines = self.env['sale.order.line'].search([])
    #
    # # Sum up the 'price_subtotal' field values using mapped()
    # total_price = sum(order_lines.mapped('price_subtotal'))
    #
    # print(total_price)

    # d = {"a": 1, "b": 2}
    # d.clear()
    # print(d)

    # d = {"a": 1, "b": 2}
    # new_d = d.copy()
    # print(new_d)

    # keys = ["a", "b", "c"]
    # d = dict.fromkeys(keys, 0)
    # print(d)

    # d = {"a": 1, "b": 2}
    # print(d.get("a"))
    # print(d.get("c", 0))

    # d = {"a": 1, "b": 2}
    # print(list(d.items()))

    # d = {"a": 1, "b": 2}
    # print(list(d.keys()))

    # d = {"a": 1, "b": 2}
    # print(list(d.values()))

    # d = {"a": 1, "b": 2}
    # print(d.pop("a"))
    # print(d)
    # print(d.pop("c", 0))

    # d = {"a": 1, "b": 2}
    # print(d.popitem())
    # print(d)

    # d = {"a": 1}
    # print(d.setdefault("a", 5))
    # print(d.setdefault("b", 5))
    # print(d)

    # d = {"a": 1}
    # d.update({"b": 2, "c": 3})
    # print(d)
    #
    # d.update([("d", 4), ("e", 5)])
    # print(d)

    # d = {"a": 1, "b": 2}
    # del d["a"]
    # print(d)

    # squares = {x: x*x for x in range(1, 6)}
    # print(squares)

    #
    # for record in self:
    #   if record.date_time_field:
    #       dt = record.date_time_field
    #       record.days_in_float = dt.day + (dt.hour / 24) + (dt.minute / 1440)

    # for record in self:
    #     if record.date_time_field:
    #         dt = record.date_time_field
    #         record.time_in_float = dt.hour + (dt.minute / 60) + (dt.second / 3600)

    # for record in self:
    #     if record.start_date_time and record.end_date_time:
    #         delta = record.end_date_time - record.start_date_time
    #         record.days_and_hours_in_float = delta.total_seconds() / 86400

    # from odoo import models, fields, api
    #
    # class SaleOrder(models.Model):
    #     _inherit = 'sale.order'
    #
    #     def confirm_draft_orders(self):
    #         """Finds all draft orders and confirms them."""
    #         draft_orders = self.search([('state', '=', 'draft')])  # ORM search method
    #         draft_orders.write({'state': 'sale'})  # ORM write method
    #         return True




