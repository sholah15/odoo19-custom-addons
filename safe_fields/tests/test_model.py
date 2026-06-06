# tests/test_model.py

from odoo import models, fields

class SafeFieldTest(models.Model):
    _name = "safe.field.test"

    name = fields.SafeChar()
    notes = fields.SafeText()

    qty = fields.SafeInteger()
    price = fields.SafeFloat()

    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ])
