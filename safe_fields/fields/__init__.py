from .safe_integer import SafeInteger
from .safe_float import SafeFloat
from .safe_monetary import SafeMonetary
from .safe_char import SafeChar
from .safe_text import SafeText

from odoo import fields

fields.SafeInteger = SafeInteger
fields.SafeFloat = SafeFloat
fields.SafeMonetary = SafeMonetary
fields.SafeChar = SafeChar
fields.SafeText = SafeText
