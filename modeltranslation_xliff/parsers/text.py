# (c) 2018, Roman Miroshnychenko <roman1972@gmail.com>
# License: MIT
"""
Dummy parser for plain text
"""
from html import unescape

__all__ = ['parse_content', 'add_xliff_tags']


def parse_content(text):
    return text


def add_xliff_tags(segment):
    return unescape(segment)  # Plain text does not require any special tags
