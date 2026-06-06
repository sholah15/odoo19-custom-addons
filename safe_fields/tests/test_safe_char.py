from odoo.tests.common import TransactionCase

PAYLOADS = [
    '<script>alert(1)</script>',
    '<img src=x onerror=alert(1)>',
    '<svg onload=alert(1)>',
    '<iframe src=javascript:alert(1)>',
]

class TestSafeChar(TransactionCase):

    def test_strip_html(self):
        rec = self.env['safe.field.test'].create({
            'name': '<script>alert(1)</script>John'
        })
        self.assertEqual(rec.name, 'John')

    def test_remove_html_tags(self):
        rec = self.env['safe.field.test'].create({
            'name': '<b>John</b>'
        })
        self.assertEqual(rec.name, 'John')

    def test_remove_zero_width(self):
        rec = self.env['safe.field.test'].create({
            'name': 'Jo\u200bhn'
        })
        self.assertEqual(rec.name, 'John')

    def test_nbsp(self):
        rec = self.env['safe.field.test'].create({
            'name': 'John\u00a0Doe'
        })
        self.assertEqual(rec.name, 'John Doe')

    def test_write_sanitized(self):
        rec = self.env['safe.field.test'].create({
            'name': 'John'
        })
        rec.write({
            'name': '<script>x</script>Doe'
        })
        self.assertEqual(rec.name, 'Doe')

    def test_mass_create(self):
        vals = []
        for i in range(100):
            vals.append({
                'name': '<b>User%s</b>' % i
            })
        records = self.env['safe.field.test'].create(vals)
        for rec in records:
            self.assertNotIn('<b>', rec.name)

    def test_xss_payloads(self):
        for payload in PAYLOADS:
            rec = self.env['safe.field.test'].create({
                'name': payload
            })
            self.assertNotIn('<script', rec.name.lower())
            self.assertNotIn('onerror', rec.name.lower())
            self.assertNotIn('onload', rec.name.lower())
