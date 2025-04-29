from odoo import models, fields, api

class ResHospital(models.Model):
    _name = "hospital.hospital"
    _description = "hospital model"

    name = fields.Char(string="Name",required=True)
    hospital_ids = fields.One2many("res.doctor","hospital_id",string="Hospital Data")

    # record = self.env['model.name'].search([('field_name', '=', value)])
    # for rec in record:
        # do something with rec


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


#
# # 🗓️ Date & Time Formula Chart for Odoo (Python)
#
# ---
#
# ### 📌 1. Import Required Libraries
# ```python
# from datetime import datetime, date, timedelta
# from odoo import fields
# ```
#
# ---
#
# ### 📌 2. Get Current Date and Time
# | Task               | Code                         |
# |--------------------|-------------------------------|
# | Today's Date        | `date.today()` or `fields.Date.today()` |
# | Current DateTime    | `datetime.now()` or `fields.Datetime.now()` |
#
# ---
#
# ### 📌 3. String and Date Conversion
# | Task               | Code Example                                       |
# |--------------------|----------------------------------------------------|
# | String ➔ Date       | `datetime.strptime('2025-04-28', '%Y-%m-%d').date()` |
# | Date ➔ String       | `date_obj.strftime('%Y-%m-%d')`                   |
#
# ---
#
# ### 📌 4. Add / Subtract Days
# | Task                | Code Example                |
# |---------------------|------------------------------|
# | Add 5 days          | `today + timedelta(days=5)`   |
# | Subtract 3 days     | `today - timedelta(days=3)`   |
#
# ---
#
# ### 📌 5. Compare Two Dates
# ```python
# if date1 > date2:
#     # date1 is after date2
# ```
#
# ---
#
# ### 📌 6. Common Format Codes (for `strftime` / `strptime`)
# | Code  | Meaning          | Example  |
# |-------|------------------|----------|
# | `%Y`  | Year (4 digits)   | 2025     |
# | `%m`  | Month (01–12)     | 04       |
# | `%d`  | Day (01–31)       | 28       |
# | `%H`  | Hour (00–23)      | 14       |
# | `%M`  | Minute (00–59)    | 45       |
# | `%S`  | Second (00–59)    | 09       |
#
# ---
#
# # ✅ Quick Mini Examples:
#
# - **Today's date**:
#   ```python
#   fields.Date.today()
#   ```
# - **Now (date + time)**:
#   ```python
#   fields.Datetime.now()
#   ```
# - **Add 7 days**:
#   ```python
#   fields.Date.today() + timedelta(days=7)
#   ```
# - **Convert string to date**:
#   ```python
#   datetime.strptime('2025-04-28', '%Y-%m-%d').date()
#   ```

#    Widget	                  When to Use
# many2many_tags	    When you want a clean tag-style selection.
# many2many_checkboxes	When options are limited and user should tick multiple easily.
# many2many_binary	    When uploading multiple files (documents/images).
# many2many_list	    Default table-style view (full record details).
# many2many_button	    When you want a quick toggle UI.
# many2many_kanban	    When records have images/status and need a rich UI.





