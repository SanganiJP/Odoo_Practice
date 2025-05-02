#
# 📋 Odoo Field Attributes Chart 📋
# 1. Common Field Attributes:
#
# Attribute	Description
# string	The label displayed for the field.
# help	Tooltip text displayed when hovering over the field.
# required	Boolean: True if the field is mandatory, False if optional.
# readonly	Boolean: True if the field is read-only, False if editable.
# default	A function or value that sets the field's default value.
# compute	A function to compute the value of the field.
# store	Boolean: If True, stores computed field value in the database.
# inverse	A function to update the field when the computed field is modified.
# copy	Boolean: True if the field should be copied when duplicating a record.
# domain	A list of conditions to restrict the selection options for the field.
# related	Refers to another field in a related model.
# ondelete	Specifies the behavior when the related record is deleted (set null, cascade, etc.).
# store	If set to True, the computed value is stored in the database.
# 2. Field Type-Specific Attributes:
# Char Field:
#
# Attribute	Description
# size	The maximum number of characters allowed.
# Text Field:
#
# Attribute	Description
# sanitize	Boolean: Whether the text content is sanitized or not (for rich-text).
# Integer / Float Field:
#
# Attribute	Description
# digits	Tuple (precision, scale) that specifies the number of digits and decimals.
# Boolean Field:
#
# Attribute	Description
# default	The default value for the Boolean field (True or False).
# Date Field:
#
# Attribute	Description
# auto_now	Boolean: Whether to automatically set the field to the current date.
# Datetime Field:
#
# Attribute	Description
# auto_now	Boolean: Automatically set the current date and time.
# Many2one Field:
#
# Attribute	Description
# comodel_name	The related model for the many2one relation.
# ondelete	Defines behavior when the related record is deleted (cascade, set null, etc.).
# domain	Restricts the related model's records to a subset.
# One2many Field:
#
# Attribute	Description
# comodel_name	The related model for the one2many relation.
# inverse_name	The field on the related model that links back to this model.
# Many2many Field:
#
# Attribute	Description
# comodel_name	The related model for the many2many relation.
# relation	The name of the intermediary table.
# ondelete	Defines behavior when a related record is deleted.
# column1	Defines the field for the first column in the relationship table.
# column2	Defines the field for the second column in the relationship table.
# 3. Other Useful Field Attributes:
#
# Attribute	Description
# states	Dict that defines the state-based visibility and behavior of the field.
# store	Store the field in the database if True (for computed fields).
# tracking	If True, tracks changes for this field in the chatter.
# related_sudo	Boolean: Whether the related field should ignore access rights.
# group_operator	The operator used in group_by for aggregate fields (like sum).
# 4. Other Field Types:
# Binary Field:
#
# Attribute	Description
# attachment	Boolean: If True, stores the file as an attachment.
# Selection Field:
#
# Attribute	Description
# selection	A list of tuples for the field's possible values.
# default	The default value from the available selection options.
#
# 📌 Example Field Definition in Model:
#
# class Product(models.Model):
#     _name = 'product.template'
#
#     name = fields.Char(string='Product Name', required=True)
#     price = fields.Float(string='Price', digits=(6, 2), default=0.0)
#     description = fields.Text(string='Description', help='Product Description')
#     category_id = fields.Many2one('product.category', string='Category', ondelete='cascade')
#     active = fields.Boolean(string='Active', default=True)
#     image = fields.Binary(string='Product Image')
#
#
# <field name="partner_id" clear="1"/>
# <field name="customer_id" readonly="1"/>
# <field name="product_name" string="Product Name"/>
# <field name="product_price" required="1"/>
# <field name="product_description" size="256"/>
# <field name="supplier_id" domain="[('supplier_rank', '>', 0)]"/>
# <field name="product_type" default="'physical'"/>
# <field name="is_active" readonly="1"/>
# <field name="order_date" compute="compute_order_date"/>
# <field name="total_amount" store="True"/>
# <field name="order_status" attrs="{'invisible': [('state', '=', 'draft')]}"/>
# <field name="partner_id" groups="base.group_user"/>
# <field name="order_lines" widget="many2many_tags"/>
# <field name="product_id" domain="[('category_id', '=', active_category)]"/>
# <field name="shipping_address" context="{'default_country_id': 1}"/>
# <field name="payment_terms" options="{'no_create': True}"/>
# <field name="customer_email" readonly="True"/>
# <field name="tags" widget="many2many_tags" editable="bottom"/>
# <field name="discount" attrs="{'readonly': [('product_type', '=', 'service')]}"/>
# <field name="shipping_method" required="1" readonly="0"/>
# <field name="supplier_id" domain="[('supplier_rank', '>', 0)]"/>
# <field name="order_date" readonly="True"/>
# <field name="amount_total" store="True" compute="compute_total_amount"/>
# <field name="account_id" context="{'default_type': 'view'}"/>
# <field name="currency_id" readonly="True" groups="base.group_user"/>
# <field name="customer_id" domain="[('active', '=', True)]"/>
# <field name="product_category" size="64" required="1"/>
# <field name="partner_id" readonly="1" context="{'default_partner_type': 'customer'}"/>
# <field name="account_balance" readonly="True"/>
# <field name="quantity" size="10" digits="(16, 2)"/>
# <field name="invoice_line_ids" widget="many2many" options="{'no_create': True}"/>
# <field name="user_id" groups="base.group_system"/>
# <field name="date_order" string="Order Date" readonly="1"/>
# <field name="is_confirmed" readonly="1" attrs="{'invisible': [('state', '=', 'draft')]}"/>
# <field name="tags" widget="many2many_tags" options="{'color_field': 'color'}"/>
# <field name="partner_id" domain="[('supplier_rank', '>', 0)]" context="{'default_type': 'contact'}"/>
# <field name="partner_id" clear="1" options="{'no_create': True}"/>
# <field name="payment_date" compute="compute_payment_date" inverse="set_payment_date"/>
# <field name="is_verified" readonly="True" default="False"/>
# <field name="company_id" readonly="True" context="{'force_company': company.id}"/>
# <field name="total_qty" store="True" compute="compute_total_qty"/>
# <field name="sale_order_ids" widget="many2many_tags" readonly="True"/>
# <field name="is_paid" readonly="1" default="False"/>
# <field name="delivery_date" required="1" attrs="{'invisible': [('state', '=', 'done')]}"/>
# <field name="product_id" domain="[('categ_id', '=', category_id)]"/>
# <field name="discount" readonly="1" options="{'no_create': True}"/>
# <field name="payment_method" required="True"/>
# <field name="payment_status" compute="compute_payment_status"/>
# <field name="shipping_address" size="128"/>
# <field name="partner_id" domain="[('active', '=', True)]"/>
# <field name="purchase_order_ids" widget="many2many_tags" readonly="True"/>


# Field Attributes Explained:
# clear="1": Clears the field value.
#
# readonly="1": Makes the field read-only.
#
# string="Product Name": Sets the label name for the field.
#
# required="1": Makes the field mandatory.
#
# size="256": Defines the maximum size of the input for char type fields.
#
# domain="[('supplier_rank', '>', 0)]": Restricts the values based on conditions (e.g., for many2one fields).
#
# default="'physical'": Sets a default value for the field.
#
# compute="compute_order_date": Specifies a computed field.
#
# store="True": Indicates the field's value is stored in the database.
#
# attrs="{'invisible': [('state', '=', 'draft')]}": Hides the field based on a condition.
#
# groups="base.group_user": Restricts field access based on user groups.
#
# widget="many2many_tags": Specifies a widget for displaying a many2many field.
#
# options="{'no_create': True}": Disables creation of new records in the many2one or many2many field.
#
# context="{'default_country_id': 1}": Sets a context for the field when creating new records.
#
#===================riban

# <!-- Draft Stage Ribbon (Default color) -->
# <widget name="web_ribbon" title="Draft" invisible="state != 'Draft'"/>
#
# <!-- Confirmed Stage Ribbon (Green background for success) -->
# <widget name="web_ribbon" title="Confirmed" bg_color="text-bg-success" invisible="state != 'confirm'"/>
#
# <!-- Done Stage Ribbon (Blue background for info) -->
# <widget name="web_ribbon" title="Completed" bg_color="text-bg-primary" invisible="state != 'done'"/>
#
# <!-- Cancelled or Lost Stage Ribbon (Red background for danger) -->
# <widget name="web_ribbon" title="Cancelled" bg_color="text-bg-danger" invisible="state != 'cancelled'"/>
#
# <!-- Pending Stage Ribbon (Yellow background for warning) -->
# <widget name="web_ribbon" title="Pending" bg_color="text-bg-warning" invisible="state != 'pending'"/>
#
# <!-- On Hold Stage Ribbon (Secondary color) -->
# <widget name="web_ribbon" title="On Hold" bg_color="text-bg-secondary" invisible="state != 'on_hold'"/>
#
# <!-- Archived Record Ribbon (Dark color) -->
# <widget name="web_ribbon" title="Archived" bg_color="text-bg-dark" invisible="active"/>

# <widget name="web_ribbon" title="Draft" invisible="state != 'draft'"/>
# <widget name="web_ribbon" title="Confirm" invisible="state != 'confirm'"/>
# <widget name="web_ribbon" title="Done" invisible="state != 'done'"/>