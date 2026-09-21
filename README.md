# Safe Fields Framework

**Safe Fields Framework** is an Odoo module that provides secure field types extending standard Odoo fields. It adds robust server-side input sanitization, strict validation, and optional OWL widget protections for the frontend.

---

## 🚀 Key Features

* **Server-Side Security:** Provides validation and sanitization independent of client-side controls.
* **Comprehensive Protection:** Protects operations coming from `create()`, `write()`, data imports, RPC calls, and external REST/Odoo APIs.
* **OWL Widgets:** Includes optional frontend widgets to prevent invalid user keystrokes in real time.

---

## 📦 Available Field Types & Widgets

### 1. `fields.SafeInteger`
Extends `fields.Integer` with:
* Enforces strict integer types.
* Rejects non-numeric values and invalid integer conversions.
* **Widget:** `widget="safe_integer"` (prevents non-digit input on the frontend).

### 2. `fields.SafeFloat`
Extends `fields.Float` with:
* Enforces float types and rejects `NaN` (Not a Number).
* Rejects positive and negative `Infinity` values.
* Blocks scientific notation input (e.g., `1e6`).
* **Widget:** `widget="safe_float"` (prevents invalid numeric keystrokes).

### 3. `fields.SafeMonetary`
Extends `fields.Monetary` with:
* Inherits float validation from `SafeFloat` (`NaN`, `Infinity`, scientific notation blocks).
* Preserves standard Odoo currency formatting.
* **Widget:** `widget="safe_monetary"`.

### 4. `fields.SafeChar` & `fields.SafeText`
Extends `fields.Char` and `fields.Text` with comprehensive text sanitization:
* Strips HTML tags, `<script>`, and `<iframe>` elements.
* Removes embedded JavaScript content and HTML event handlers (e.g., `onload`, `onerror`).
* Removes invisible and zero-width Unicode characters.
* Normalizes Unicode text.
* Trims leading and trailing whitespace.

---

## 🛡️ Security Benefits

* **Prevents XSS:** Significantly reduces the risk of Stored Cross-Site Scripting (XSS) attacks.
* **Data Integrity:** Blocks malformed numbers, `NaN`, or infinite values from corrupting database records and reporting engines.
* **API Safety:** Ensures clean data ingestion even when bypasses are attempted on the frontend or via direct API calls.

---

## 💻 Usage Example

### Python Model Definition

```python
from odoo import models, fields

class SafeFieldsTester(models.Model):
    _name = "safe.fields.tester"
    _description = "Safe Fields Test Model"

    name = fields.SafeChar(string="Name")
    notes = fields.SafeText(string="Notes")
    qty = fields.SafeInteger(string="Quantity")
    price = fields.SafeFloat(string="Unit Price")
    amount = fields.SafeMonetary(string="Amount", currency_field="currency_id")
    currency_id = fields.Many2one("res.currency", string="Currency")
```

### XML Form View Definition

```xml
<record id="safe_fields_tester_form" model="ir.ui.view">
    <field name="name">safe.fields.tester.form</field>
    <field name="model">safe.fields.tester</field>
    <field name="arch" type="xml">
        <form>
            <sheet>
                <group>
                    <field name="name"/>
                    <field name="notes"/>
                    <field name="distance" widget="safe_float"/>
                </group>
                <group>
                    <field name="qty" widget="safe_integer"/>
                    <field name="price" widget="safe_monetary" options="{'currency_field': 'currency_id'}"/>
                    <field name="currency_id"/>
                </group>
            </sheet>
        </form>
    </field>
</record>
```

---

## ⚠️ Important Notes

* **Plain Text Scope:** `SafeChar` and `SafeText` are designed specifically for plain text content.
* **Rich Text Formatting:** If your business logic requires HTML/rich text formatting, use Odoo's native `fields.Html` with Odoo's built-in HTML sanitizer instead of `SafeChar` or `SafeText`.