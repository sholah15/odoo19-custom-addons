# -*- coding: utf-8 -*-
"""Inisialisasi modul fields.

Mendaftarkan field kustom (SafeInteger, SafeFloat, SafeMonetary, SafeChar, SafeText)
ke namespace odoo.fields secara langsung agar dapat digunakan layaknya field bawaan.
"""

from .safe_integer import SafeInteger
from .safe_float import SafeFloat
from .safe_monetary import SafeMonetary
from .safe_char import SafeChar
from .safe_text import SafeText

# pyrefly: ignore [missing-import]
from odoo import fields

# Inject class custom fields ke odoo.fields
fields.SafeInteger = SafeInteger
fields.SafeFloat = SafeFloat
fields.SafeMonetary = SafeMonetary
fields.SafeChar = SafeChar
fields.SafeText = SafeText
