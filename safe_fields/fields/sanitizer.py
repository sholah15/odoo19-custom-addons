# -*- coding: utf-8 -*-
"""Fungsi pembantu (utility) untuk membersihkan teks input dari karakter

berbahaya atau karakter tersembunyi yang tidak diinginkan.
"""

import unicodedata
import re
from lxml.html.clean import Cleaner
from lxml import html

# Konfigurasi lxml Cleaner untuk menyaring tag HTML berbahaya
_cleaner = Cleaner(
    scripts=True,
    javascript=True,
    comments=True,
    style=True,
    links=True,
    meta=True,
    page_structure=False,
    safe_attrs_only=True,
)

# Karakter non-printing/tersembunyi yang akan dihapus dari input
INVISIBLE_CHARS = [
    '\u200b',  # zero width space
    '\u200c',  # zero width non-joiner
    '\u200d',  # zero width joiner
    '\u202e',  # right-to-left override
]


def sanitize_text_input(value):
    """Membersihkan nilai input teks dari karakter unicode tersembunyi,

    normalisasi spasi, dan menghapus tag HTML berbahaya demi keamanan data.

    Args:
        value (str): Teks mentah yang akan dibersihkan.

    Returns:
        str: Teks yang telah dibersihkan dan dipangkas spasi berlebihnya.
    """
    if not value:
        return value

    # Normalisasi unicode ke format NFC
    value = unicodedata.normalize("NFC", value)

    # Ganti Non-breaking Space (NBSP) dengan spasi biasa
    value = value.replace('\u00a0', ' ')

    # Hapus seluruh karakter tersembunyi yang terdefinisi
    for ch in INVISIBLE_CHARS:
        value = value.replace(ch, '')

    # Bersihkan elemen HTML secara aman menggunakan lxml Cleaner
    try:
        doc = html.fromstring(value)
        doc = _cleaner.clean_html(doc)
        value = doc.text_content()
    except Exception:
        # Fallback menggunakan regex jika lxml gagal memproses
        value = re.sub(r'<[^>]*?>', '', value)

    # Pangkas spasi di awal dan akhir teks
    value = value.strip()

    return value
