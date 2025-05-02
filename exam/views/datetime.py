# from datetime import datetime, date, time, timedelta
# from odoo.fields import Date, Datetime
#
# # Related to datetime conversion
#
# today = date.today()  # Only date
# now = datetime.now()  # Full date + time
# utc_now = Datetime.now()  # Odoo style (UTC safe)
#
# future_date = date.today() + timedelta(days=5)
# # Subtract 2 hours
# past_time = datetime.now() - timedelta(hours=2)
#
# now = datetime.now()
# formatted_date = now.strftime('%Y-%m-%d')   # e.g., '2025-04-28'
# formatted_time = now.strftime('%H:%M:%S')   # e.g., '14:25:00'
#
# date_string = '2025-04-28 14:30:00'
# date_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
#
# records = self.env['your.model'].search([
#     ('create_date', '>=', Date.today())
# ])

# _prepare_merge_moves_distinct_fields