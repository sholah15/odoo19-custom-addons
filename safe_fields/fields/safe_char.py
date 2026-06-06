from odoo import fields
from odoo.exceptions import ValidationError
from .sanitizer import sanitize_text_input


class SafeChar(fields.Char):

    type = 'safe_char'

    def convert_to_cache(self, value, record, validate=True):
        value = super().convert_to_cache(value, record, validate)

        if value:
            value = sanitize_text_input(value)

        return value

    def convert_to_write(self, value, record):
        value = super().convert_to_write(value, record)

        if value:
            value = sanitize_text_input(value)

        return value
