# (c) 2018, Roman Miroshnychenko <roman1972@gmail.com>
# License: MIT
"""
Functions for splitting blocks of text into translation segments

This module uses sent_tokenize function from NLTK package that splits text
into sentences that correspond to translation segments in CAT tools.
"""

from nltk import download
from nltk.tokenize import sent_tokenize

try:
    sent_tokenize('Test.')
except LookupError:
    download('punkt')

__all__ = ['NLTK_SUPPORTED_LANGUAGES', 'is_supported_language', 'segment_text']

NLTK_SUPPORTED_LANGUAGES = {
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'et': 'estonian',
    'fi': 'finnish',
    'fr': 'french',
    'de': 'german',
    'el': 'greek',
    'it': 'italian',
    'no': 'norwegian',
    'pl': 'polish',
    'pt': 'portuguese',
    'sl': 'slovene',
    'es': 'spanish',
    'sv': 'swedish',
    'tr': 'turkish'
}


def is_supported_language(lang_code):
    # type: (str) -> bool
    """
    Check if a language code is supported by NLTK

    :param lang_code: language code in ll or ll-CC format
    :return: check result
    """
    return lang_code[:2] in NLTK_SUPPORTED_LANGUAGES


def segment_text(text, lang_code):
    # type: (str, str) -> list
    """
    Split text into translation segements using NLTK

    :param text: text to segment
    :param lang_code: language code for the text
    :return: the list of translation segments
    :raises LookupError: if the text language is not supported by NLTK
    """
    language = NLTK_SUPPORTED_LANGUAGES.get(lang_code[:2])
    if not language:
        raise LookupError(
            'Language "{}" is not supported by NLTK!'.format(lang_code)
        )
    return sent_tokenize(text, language)
