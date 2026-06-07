from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tools.translate import _
import math


class SafeInteger(fields.Integer):
    pass

    def convert_to_cache(self, value, record, validate=True):
        value = super().convert_to_cache(value, record, validate)
        if value is None:
            return value
        if not isinstance(value, int):
            raise ValidationError(
                _("Field %s must be an integer.") % self.string
            )
        return value

    def convert_to_write(self, value, record):
        value = super().convert_to_write(value, record)
        if value is None:
            return value
        if not isinstance(value, int):
            raise ValidationError(
                _("Field %s must be an integer.") % self.string
            )
        return value
