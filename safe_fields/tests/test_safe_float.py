# -*- coding: utf-8 -*-
# pyrefly: ignore [missing-import]
from odoo.exceptions import ValidationError
# pyrefly: ignore [missing-import]
from odoo.tests.common import TransactionCase


class TestSafeFloat(TransactionCase):
    """Kelas pengujian untuk memverifikasi fungsionalitas SafeFloat."""

    def test_float_ok(self):
        """Memastikan nilai float yang valid dapat disimpan dengan benar."""
        rec = self.env['safe.field.test'].create({
            'price': 1.25
        })
        self.assertEqual(rec.price, 1.25)

    def test_nan_rejected(self):
        """Memastikan input NaN (Not a Number) memicu ValidationError."""
        import math
        with self.assertRaises(ValidationError):
            self.env['safe.field.test'].create({
                'price': math.nan
            })

    def test_inf_rejected(self):
        """Memastikan input Infinity memicu ValidationError."""
        import math
        with self.assertRaises(ValidationError):
            self.env['safe.field.test'].create({
                'price': math.inf
            })

    def test_write_sanitized(self):
        """Memastikan penulisan/pembaruan (write) nilai float bekerja dengan benar."""
        rec = self.env['safe.field.test'].create({
            'price': 1.25
        })
        rec.write({
            'price': 2.50
        })
        self.assertEqual(rec.price, 2.50)

    def test_mass_create(self):
        """Memastikan pembuatan batch (mass create) mencatat data dengan nilai float yang sesuai."""
        vals = []
        for i in range(100):
            vals.append({
                'price': i * 1.5
            })
        records = self.env['safe.field.test'].create(vals)
        for index, rec in enumerate(records):
            self.assertEqual(rec.price, index * 1.5)
