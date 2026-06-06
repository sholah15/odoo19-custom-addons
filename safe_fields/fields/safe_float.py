from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tools.translate import _
import math


class SafeFloat(fields.Float):

    type = 'safe_float'

    def convert_to_cache(self, value, record, validate=True):
        value = super().convert_to_cache(value, record, validate)

        if value is None:
            return value

        if math.isnan(value) or math.isinf(value):
            raise ValidationError(
                _("Field %s contains invalid number.") % self.string
            )

        return value
