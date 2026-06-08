from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tools.translate import _
import math


class SafeInteger(fields.Integer):
    pass

    def convert_to_cache(self, value, record, validate=True):
        try:
            value = super().convert_to_cache(value, record, validate)
        except (ValueError, TypeError):
            # Ubah ValueError (karena diisi huruf) dan TypeError menjadi ValidationError
            raise ValidationError(
                _("Field %s must be an integer.") % self.string
            )
        if value is None:
            return value
        if not isinstance(value, int):
            raise ValidationError(
                _("Field %s must be an integer.") % self.string
            )
        return value

    def convert_to_write(self, value, record):
        try:
            value = super().convert_to_write(value, record)
        except (ValueError, TypeError):
            # Ubah ValueError (karena diisi huruf) dan TypeError menjadi ValidationError
            raise ValidationError(
                _("Field %s must be an integer.") % self.string
            )
        if value is None:
            return value
        if not isinstance(value, int):
            raise ValidationError(
                _("Field %s must be an integer.") % self.string
            )
        return value
