# # Odoo - Special Commands on relational fields (One2many / Many2many)
# # This file contains examples for (0,0), (1,id), (2,id), (3,id), (4,id), (5,), (6,0,[ids])
#
# # Suppose we have a model with a One2many field 'line_ids'
# # Example record
# record = self.env['your.model'].browse(record_id)
#
# # (0, 0, { values }) -> Create a new record and link it
# record.write({
#     'line_ids': [(0, 0, {
#         'name': 'New Line',
#         'quantity': 10,
#     })]
# })
# # --> Creates a new linked record with given values.
#
# # (1, ID, { values }) -> Update an existing linked record
# record.write({
#     'line_ids': [(1, existing_line_id, {
#         'quantity': 20,
#     })]
# })
# # --> Updates the existing linked record having ID = existing_line_id.
#
# # (2, ID) -> Remove and delete the linked record
# record.write({
#     'line_ids': [(2, existing_line_id)]
# })
# # --> Deletes the linked record from database and removes its link.
#
# # (3, ID) -> Cut the link but do not delete the record
# record.write({
#     'line_ids': [(3, existing_line_id)]
# })
# # --> Only removes the link; record stays in database.
#
# # (4, ID) -> Link to an existing record
# record.write({
#     'line_ids': [(4, existing_line_id)]
# })
# # --> Links an already existing record to this record.
#
# # (5,) -> Unlink all linked records
# record.write({
#     'line_ids': [(5,)]
# })
# # --> Removes all links. Like calling (3, ID) for every linked record.
#
# # (6, 0, [IDs]) -> Replace list of linked IDs
# record.write({
#     'line_ids': [(6, 0, [id1, id2, id3])]
# })
# # --> Clears old links and adds links to id1, id2, id3.
#
# # ------------------------------------------------------------------------------------
# # Quick Reference:
# # (0, 0, {values}) : Create and link new record.
# # (1, ID, {values}): Update existing linked record.
# # (2, ID)         : Delete and unlink the record.
# # (3, ID)         : Unlink without deleting.
# # (4, ID)         : Link to an existing record.
# # (5,)            : Unlink all records.
# # (6, 0, [IDs])   : Replace all links with new ones.
# # ------------------------------------------------------------------------------------


# # Get all sale orders
# sale_orders = self.env['sale.order'].search([])
#
# # Step by step using filtered, mapped, lambda, and sum
# confirmed_orders = sale_orders.filtered(lambda so: so.state == 'sale')  # Only confirmed orders
#
# order_lines = confirmed_orders.mapped('order_line')  # All order lines from confirmed orders
#
# filtered_lines = order_lines.filtered(lambda line: line.product_uom_qty > 10)  # Only lines with qty > 10
#
# total_amount = sum(filtered_lines.mapped('price_subtotal'))  # Sum of their subtotal prices
#
# # Print or use the total
# print('Total amount for lines with qty > 10:', total_amount)


# # -*- coding: utf-8 -*-
# from odoo import models, fields, api
#
# class YourModel(models.Model):
#     _name = 'your.model'
#     _description = 'Your Model'
#
#     # Computed field to decide button class
#     button_class = fields.Char(string="Button Class", compute="_compute_button_class")
#
#     @api.depends()
#     def _compute_button_class(self):
#         """Compute button class based on system parameter."""
#         param_value = self.env['ir.config_parameter'].sudo().get_param('my_module.show_buttons')
#         for record in self:
#             if param_value == 'True':
#                 record.button_class = 'btn-primary'
#             else:
#                 record.button_class = 'btn-secondary'
#
#     def action_button(self):
#         """Action to be triggered on button click."""
#         # You can add your custom button logic here
#         return True

# ===============================
# SYSTEM PARAMETER XML
# ===============================

'''
Save this part into your_module/data/system_parameter_data.xml

<?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <data noupdate="1">
        <!-- Create system parameter 'my_module.show_buttons' with default value True -->
        <record id="system_parameter_show_buttons" model="ir.config_parameter">
            <field name="key">my_module.show_buttons</field>
            <field name="value">True</field>
        </record>
    </data>
</odoo>
'''

# ===============================
# FORM VIEW XML
# ===============================

'''
Save this part into your_module/views/your_model_views.xml

<?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <record id="view_form_your_model" model="ir.ui.view">
        <field name="name">your.model.form</field>
        <field name="model">your.model</field>
        <field name="arch" type="xml">
            <form string="Your Model">

                <!-- Button shown when parameter is True (Primary button) -->
                <button name="action_button"
                        string="Click Me"
                        type="object"
                        class="btn btn-primary"
                        attrs="{'invisible': [('button_class', '!=', 'btn-primary')]}"/>

                <!-- Button shown when parameter is False (Secondary button) -->
                <button name="action_button"
                        string="Click Me"
                        type="object"
                        class="btn btn-secondary"
                        attrs="{'invisible': [('button_class', '!=', 'btn-secondary')]}"/>

            </form>
        </field>
    </record>
</odoo>
'''

# ===============================
# MANIFEST FILE (__manifest__.py) UPDATE
# ===============================

'''
Make sure your __manifest__.py has:

'data': [
    'data/system_parameter_data.xml',
    'views/your_model_views.xml',
],
'''

