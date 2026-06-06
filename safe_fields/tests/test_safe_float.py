from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase

class TestSafeFloat(TransactionCase):

    def test_float_ok(self):
        rec = self.env['safe.field.test'].create({
            'price': 1.25
        })
        self.assertEqual(rec.price, 1.25)

    def test_nan_rejected(self):
        import math
        with self.assertRaises(ValidationError):
            self.env['safe.field.test'].create({
                'price': math.nan
            })

    def test_inf_rejected(self):
        import math
        with self.assertRaises(ValidationError):
            self.env['safe.field.test'].create({
                'price': math.inf
            })
    
    def test_write_sanitized(self):
        rec = self.env['safe.field.test'].create({
            'price': 1.25
        })
        rec.write({
            'price': 2.50
        })
        self.assertEqual(rec.price, 2.50)

    def test_mass_create(self):
        vals = []
        for i in range(100):
            vals.append({
                'price': i * 1.5
            })
        records = self.env['safe.field.test'].create(vals)
        for rec in records:
            self.assertEqual(rec.price, rec.price)
