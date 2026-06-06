from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase

class TestSafeInteger(TransactionCase):

    def test_integer_ok(self):
        rec = self.env['safe.field.test'].create({
            'qty': 10
        })
        self.assertEqual(rec.qty, 10)

    def test_integer_invalid_string(self):
        with self.assertRaises(ValidationError):
            self.env['safe.field.test'].create({
                'qty': 'abc'
            })

    def test_integer_invalid_float(self):
        with self.assertRaises(ValidationError):
            self.env['safe.field.test'].create({
                'qty': 1.5
            })
    
    def test_write_sanitized(self):
        rec = self.env['safe.field.test'].create({
            'qty': 10
        })
        rec.write({
            'qty': 20
        })
        self.assertEqual(rec.qty, 20)
    
    def test_mass_create(self):
        vals = []
        for i in range(100):
            vals.append({
                'qty': i
            })
        records = self.env['safe.field.test'].create(vals)
        for rec in records:
            self.assertEqual(rec.qty, i)
