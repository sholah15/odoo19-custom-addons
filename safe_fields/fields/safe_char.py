# -*- coding: utf-8 -*-
# pyrefly: ignore [missing-import]
from odoo import fields
from .sanitizer import sanitize_text_input


class SafeChar(fields.Char):
    """Field Char kustom yang secara otomatis membersihkan input karakter tunggal/pendek

    dari karakter tersembunyi, spasi tidak standar, dan tag HTML berbahaya.
    """

    def convert_to_cache(self, value, record, validate=True):
        """Membersihkan nilai input karakter saat memuat atau menyimpan ke cache."""
        value = super().convert_to_cache(value, record, validate)
        if value:
            value = sanitize_text_input(value)
        return value

    def convert_to_write(self, value, record):
        """Membersihkan nilai input karakter saat menulis (write) ke database."""
        value = super().convert_to_write(value, record)
        if value:
            value = sanitize_text_input(value)
        return value
