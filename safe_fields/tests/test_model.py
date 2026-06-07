from odoo import models, fields


class SafeFieldTest(models.Model):
    _name = "safe.field.test"
    _description = "Safe Field Test"

    name = fields.SafeChar()
    notes = fields.SafeText()

    qty = fields.SafeInteger()
    price = fields.SafeFloat()
    currency_id = fields.Many2one("res.currency")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ])
