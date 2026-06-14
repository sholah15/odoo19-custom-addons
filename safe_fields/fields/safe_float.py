# -*- coding: utf-8 -*-
# pyrefly: ignore [missing-import]
from odoo import fields
# pyrefly: ignore [missing-import]
from odoo.exceptions import ValidationError
# pyrefly: ignore [missing-import]
from odoo.tools.translate import _
import math


class SafeFloat(fields.Float):
    """Field Float kustom yang melakukan validasi tambahan untuk mencegah

    nilai numerik tidak valid seperti NaN (Not a Number) atau Infinity.
    """

    def convert_to_cache(self, value, record, validate=True):
        """Mengonversi nilai menjadi nilai cache dengan validasi tambahan terhadap NaN dan Infinity."""
        value = super().convert_to_cache(value, record, validate)
        if value is None:
            return value
        if math.isnan(value) or math.isinf(value):
            raise ValidationError(
                _("Field %s contains invalid number.") % self.string
            )
        return value
