import unicodedata
import re
from lxml.html.clean import Cleaner
from lxml import html


# Cleaner config
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


INVISIBLE_CHARS = [
    '\u200b',  # zero width space
    '\u200c',
    '\u200d',
    '\u202e',  # RLO
]


def sanitize_text_input(value):
    if not value:
        return value

    # Normalize unicode
    value = unicodedata.normalize("NFC", value)

    # Replace NBSP with regular space
    value = value.replace('\u00a0', ' ')

    # Remove invisible chars
    for ch in INVISIBLE_CHARS:
        value = value.replace(ch, '')

    # Remove HTML safely
    try:
        doc = html.fromstring(value)
        doc = _cleaner.clean_html(doc)
        value = doc.text_content()
    except Exception:
        # fallback if parsing fails
        value = re.sub(r'<[^>]*?>', '', value)

    # Strip whitespace
    value = value.strip()

    return value
