from odoo.tests.common import TransactionCase

PAYLOADS = [
    '<script>alert(1)</script>',
    '<img src=x onerror=alert(1)>',
    '<svg onload=alert(1)>',
    '<iframe src=javascript:alert(1)>',
]


class TestSafeText(TransactionCase):

    def test_script_removed(self):
        rec = self.env['safe.field.test'].create({
            'notes': '<script>alert(1)</script>Hello'
        })
        self.assertEqual(rec.notes, 'Hello')

    def test_iframe_removed(self):
        rec = self.env['safe.field.test'].create({
            'notes': '<iframe src=x></iframe>Hello'
        })
        self.assertEqual(rec.notes, 'Hello')

    def test_write_sanitized(self):
        rec = self.env['safe.field.test'].create({
            'notes': 'John'
        })
        rec.write({
            'notes': '<script>x</script>Doe'
        })
        self.assertEqual(rec.notes, 'Doe')

    def test_mass_create(self):
        vals = []
        for i in range(100):
            vals.append({
                'notes': '<b>User%s</b>' % i
            })
        records = self.env['safe.field.test'].create(vals)
        for rec in records:
            self.assertNotIn('<b>', rec.notes)

def test_xss_payloads(self):
    for payload in PAYLOADS:
        rec = self.env['safe.field.test'].create({
            'notes': payload
        })
        self.assertNotIn('<script', rec.notes.lower())
        self.assertNotIn('onerror', rec.notes.lower())
        self.assertNotIn('onload', rec.notes.lower())
