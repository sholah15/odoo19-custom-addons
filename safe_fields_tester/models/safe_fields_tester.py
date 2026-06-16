# pyrefly: ignore [missing-import]
from odoo import models, fields

class SafeFieldsTester(models.Model):
    _name = "safe.fields.tester"
    _description = "Safe Fields Tester"

    name = fields.SafeChar("Name")
    notes = fields.SafeText("Notes")
    distance = fields.SafeFloat("Distance (KM)")
    qty = fields.SafeInteger("Quantity")
    price = fields.SafeMonetary("Price")
    currency_id = fields.Many2one("res.currency", "Currency")
    

