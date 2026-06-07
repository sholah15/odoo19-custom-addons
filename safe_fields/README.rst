Safe Fields Framework
=====================

This module provides secure field types that extend standard Odoo fields
with additional input sanitization, validation, and frontend protection.

Available Field Types
---------------------

* fields.SafeInteger
* fields.SafeFloat
* fields.SafeMonetary
* fields.SafeChar
* fields.SafeText

SafeInteger
-----------

Extends fields.Integer with:

* Integer type enforcement.
* Rejects non-numeric values.
* Rejects invalid integer conversions.
* Optional OWL widget to prevent non-digit input.
* Protection for create(), write(), import, RPC, and API operations.

SafeFloat
---------

Extends fields.Float with:

* Float type enforcement.
* Rejects NaN (Not a Number).
* Rejects positive and negative Infinity values.
* Optional OWL widget to prevent invalid numeric input.
* Blocks scientific notation input (e.g. 1e6).
* Protection for create(), write(), import, RPC, and API operations.

SafeMonetary
------------

Extends fields.Monetary with:

* Float validation inherited from SafeFloat.
* Rejects NaN and Infinity values.
* Optional OWL widget to prevent invalid monetary input.
* Blocks scientific notation input.
* Preserves standard Odoo currency formatting.
* Protection for create(), write(), import, RPC, and API operations.

SafeChar and SafeText
---------------------

Extends fields.Char and fields.Text with text sanitization:

* Removes HTML tags.
* Removes <script> elements.
* Removes <iframe> elements.
* Removes embedded JavaScript content.
* Removes HTML event handlers.
* Removes invisible Unicode characters.
* Removes zero-width characters.
* Normalizes Unicode text.
* Trims leading and trailing whitespace.

Security Benefits
-----------------

* Reduces risk of stored XSS attacks.
* Prevents invalid numeric values from entering the database.
* Improves data consistency.
* Protects data received from forms, imports, RPC calls, and external APIs.
* Provides server-side protection independent of client-side controls.

Example
-------

.. code:: python

    from odoo import fields

    qty = fields.SafeInteger(string="Quantity")
    price = fields.SafeFloat(string="Unit Price")
    amount = fields.SafeMonetary(
        string="Amount",
        currency_field="currency_id"
    )
    name = fields.SafeChar(string="Name")
    notes = fields.SafeText(string="Notes")

.. code:: xml

    <record model="ir.ui.view" id="safe_fields_tester_form">
      <field name="name">safe.fields.tester.form</field>
      <field name="model">safe.fields.tester</field>
      <field name="arch" type="xml">
        <form>
            <sheet>
                <group>
                    <field name="name"/>
                    <field name="notes"/>
                    <field name="distance" widget="safe_float"/>
                </group>
                <group>
                    <field name="qty" widget="safe_integer"/>
                    <field name="price" widget="safe_monetary" options="{'currency_field': 'currency_id'}"/>
                    <field name="currency_id"/>
                </group>
            </sheet>
        </form>
      </field>
    </record>

Notes
-----

SafeChar and SafeText are intended for plain text content.

If rich text formatting is required, use fields.Html with Odoo's built-in
HTML sanitization instead of SafeChar or SafeText.
