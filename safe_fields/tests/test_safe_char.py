# -*- coding: utf-8 -*-
# pyrefly: ignore [missing-import]
from odoo.tests.common import TransactionCase

PAYLOADS = [
    '<script>alert(1)</script>',
    '<img src=x onerror=alert(1)>',
    '<svg onload=alert(1)>',
    '<iframe src=javascript:alert(1)>',
]


class TestSafeChar(TransactionCase):
    """Kelas pengujian untuk memverifikasi fungsionalitas SafeChar (sanitasi karakter)."""

    def test_strip_html(self):
        """Memastikan tag script beserta isinya dihapus sepenuhnya."""
        rec = self.env['safe.field.test'].create({
            'name': '<script>alert(1)</script>John'
        })
        self.assertEqual(rec.name, 'John')

    def test_remove_html_tags(self):
        """Memastikan tag HTML biasa dihapus tetapi isinya tetap dipertahankan."""
        rec = self.env['safe.field.test'].create({
            'name': '<b>John</b>'
        })
        self.assertEqual(rec.name, 'John')

    def test_remove_zero_width(self):
        """Memastikan karakter zero-width space dihapus dari input."""
        rec = self.env['safe.field.test'].create({
            'name': 'Jo\u200bhn'
        })
        self.assertEqual(rec.name, 'John')

    def test_nbsp(self):
        """Memastikan karakter non-breaking space (NBSP) dikonversi menjadi spasi biasa."""
        rec = self.env['safe.field.test'].create({
            'name': 'John\u00a0Doe'
        })
        self.assertEqual(rec.name, 'John Doe')

    def test_write_sanitized(self):
        """Memastikan pembersihan (sanitasi) juga diterapkan saat melakukan pembaruan (write)."""
        rec = self.env['safe.field.test'].create({
            'name': 'John'
        })
        rec.write({
            'name': '<script>x</script>Doe'
        })
        self.assertEqual(rec.name, 'Doe')

    def test_mass_create(self):
        """Memastikan pembuatan batch (mass create) membersihkan data HTML dari nama."""
        vals = []
        for i in range(100):
            vals.append({
                'name': '<b>User%s</b>' % i
            })
        records = self.env['safe.field.test'].create(vals)
        for rec in records:
            self.assertNotIn('<b>', rec.name)

    def test_xss_payloads(self):
        """Memastikan berbagai payload XSS umum dibersihkan dengan aman."""
        for payload in PAYLOADS:
            rec = self.env['safe.field.test'].create({
                'name': payload
            })
            self.assertNotIn('<script', rec.name.lower())
            self.assertNotIn('onerror', rec.name.lower())
            self.assertNotIn('onload', rec.name.lower())
