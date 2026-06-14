# -*- coding: utf-8 -*-
# pyrefly: ignore [missing-import]
from odoo.exceptions import ValidationError
# pyrefly: ignore [missing-import]
from odoo.tests.common import TransactionCase


class TestSafeInteger(TransactionCase):
    """Kelas pengujian untuk memverifikasi fungsionalitas SafeInteger."""

    def test_integer_ok(self):
        """Memastikan nilai integer yang valid dapat disimpan dengan benar."""
        rec = self.env['safe.field.test'].create({
            'qty': 10
        })
        self.assertEqual(rec.qty, 10)

    def test_integer_invalid_string(self):
        """Memastikan input string non-numerik memicu ValidationError."""
        with self.assertRaises(ValidationError):
            self.env['safe.field.test'].create({
                'qty': 'abc'
            })

    def test_integer_invalid_float(self):
        """Memastikan input angka pecahan (float) memicu ValidationError."""
        with self.assertRaises(ValidationError):
            self.env['safe.field.test'].create({
                'qty': 1.5
            })

    def test_write_sanitized(self):
        """Memastikan penulisan/pembaruan (write) nilai integer bekerja dengan benar."""
        rec = self.env['safe.field.test'].create({
            'qty': 10
        })
        rec.write({
            'qty': 20
        })
        self.assertEqual(rec.qty, 20)

    def test_mass_create(self):
        """Memastikan pembuatan batch (mass create) mencatat data dengan nilai yang sesuai."""
        vals = []
        for i in range(100):
            vals.append({
                'qty': i
            })
        records = self.env['safe.field.test'].create(vals)
        for index, rec in enumerate(records):
            self.assertEqual(rec.qty, index)
