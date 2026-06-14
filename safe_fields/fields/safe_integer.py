# -*- coding: utf-8 -*-
# pyrefly: ignore [missing-import]
from odoo import fields
# pyrefly: ignore [missing-import]
from odoo.exceptions import ValidationError
# pyrefly: ignore [missing-import]
from odoo.tools.translate import _


class SafeInteger(fields.Integer):
    """Field Integer kustom yang memastikan nilai yang dimasukkan/ditulis

    adalah tipe integer (angka bulat) yang valid, serta mengubah kesalahan konversi
    (ValueError/TypeError) menjadi ValidationError Odoo yang lebih ramah pengguna.
    """

    def convert_to_cache(self, value, record, validate=True):
        """Validasi dan konversi nilai input saat memuat atau menyimpan ke cache."""
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
        """Validasi dan konversi nilai saat menulis (write) ke database."""
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
