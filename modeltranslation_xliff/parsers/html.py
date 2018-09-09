# (c) 2018, Roman Miroshnychenko <roman1972@gmail.com>
# License: MIT
"""
Parser for extracting translatable text from HTML content
"""
import logging
import re
import types
from html import escape, unescape
from html.parser import HTMLParser

__all__ = ['parse_content', 'add_xliff_tags']

INLINE_TAGS = (
    'a', 'abbr', 'acronym', 'applet', 'b', 'bdo', 'big', 'blink',
    'cite', 'code', 'del', 'dfn', 'em', 'embed', 'face', 'font', 'i',
    'iframe', 'img', 'ins', 'kbd', 'map', 'nobr', 'object',
    'param', 'q', 'rb', 'rbc', 'rp', 'rt', 'rtc', 'ruby', 's', 'samp', 'select',
    'small', 'span', 'spacer', 'strike', 'strong', 'sub', 'sup', 'symbol',
    'tt', 'u', 'var', 'wbr'
)

SELF_CLOSING_TAGS = (
    'area',
    'base',
    'br',
    'col',
    'command',
    'embed',
    'hr',
    'img',
    'input',
    'keygen',
    'link',
    'meta',
    'param',
    'source',
    'track',
    'wbr',
)

IGNORE_BLOCK_TAGS = ('script', 'style')

charset_re = re.compile(rb'<meta[^>]+charset="?([\w-]+)"[^>]*>', re.I)
whitespace_re = re.compile(r'^\s+$', re.U)
tag_string_re = re.compile(r'^(<[^>]*>)$')
tag_re = re.compile(r'(<[^>]+>)')
open_tag_re = re.compile(r'<(\w+)[^>]*>')
close_tag_re = re.compile(r'</(\w+)>')
entity_re = re.compile(r'(&#?\w+?;)')
pre_code_re = re.compile(r'^<pre[^>]*>\s*?<code[^>]*>', re.I)


class ContentParser(HTMLParser):
    """
    Extracts translatable blocks of text from HTML markup
    """
    def __init__(self):
        super().__init__(convert_charrefs=False)

    @property
    def content_list(self):
        return self._content_list

    def handle_starttag(self, tag, attrs):
        if (tag in INLINE_TAGS and self._current_block) or tag == 'pre':
            self._current_block += self.get_starttag_text()
        elif tag in IGNORE_BLOCK_TAGS:
            self._ignore_block = True
        elif tag == 'br':
            self._finish_block()
        elif tag in ('meta', 'img'):
            self._process_translatable_attrs(attrs)

    def handle_startendtag(self, tag, attrs):
        if tag in INLINE_TAGS and self._current_block:
            self._current_block += self.get_starttag_text()
        elif tag == 'br':
            self._finish_block()
        elif tag in ('meta', 'img'):
            self._process_translatable_attrs(attrs)

    def handle_endtag(self, tag):
        if tag in INLINE_TAGS or tag == 'pre':
            self._current_block += '</{}>'.format(tag)
            if tag == 'pre':
                self._finish_block()
        elif tag in IGNORE_BLOCK_TAGS:
            self._ignore_block = False
        elif self._current_block:
            self._finish_block()

    def handle_data(self, data):
        if not self._ignore_block and not whitespace_re.search(data):
            self._current_block += data

    def handle_charref(self, name):
        self._current_block += '&#' + name + ';'

    def handle_entityref(self, name):
        self._current_block += '&' + name + ';'

    def error(self, message):
        logging.error(message)

    def _finish_block(self):
        self._content_list.append(self._current_block.strip(' \r\n'))
        self._current_block = ''
        self._ignore_block = False

    def _process_translatable_attrs(self, attrs):
        attrs_dict = dict(attrs)
        if attrs_dict.get('description'):
            self._current_block += attrs_dict['description']
            self._finish_block()
        elif attrs_dict.get('keywords'):
            self._current_block += attrs_dict['keywords']
            self._finish_block()
        elif attrs_dict.get('http-equiv') == 'keywords':
            self._current_block += attrs_dict['content']
            self._finish_block()
        elif attrs_dict.get('alt'):
            self._current_block += attrs_dict['alt']
            self._finish_block()

    def reset(self):
        super().reset()
        self._content_list = []
        self._current_block = ''
        self._ignore_block = False

    def close(self):
        if self._current_block and not whitespace_re.search(self._current_block):
            self._finish_block()
        super().close()


content_parser = ContentParser()


def parse_content(html):
    # type: (str) -> types.GeneratorType
    """
    Extract translatable segments from a HTML document

    :param html: HTML document
    :return: generator that yields translatable blocks
    """
    content_parser.reset()
    content_parser.feed(html)
    content_parser.close()
    for item in content_parser.content_list:
        # Skip <pre><code> blocks
        if pre_code_re.search(item) is None:
            if not tag_string_re.search(item):
                yield item


def find_tag(tag_name, tags_stack):
    # type: (str, list) -> int
    """
    Find the closest opening tag in a tags stack
    Search is done from the end of the stack.

    :param tag_name: tag name
    :param tags_stack: tags stack
    :return: opening tag index or -1
    """
    i = len(tags_stack) - 1
    for item in reversed(tags_stack):
        if tag_name == item[0]:
            return i
        i -= 1
    return -1


def add_t_tags(segment):
    # type: (str) -> str
    """
    Add <bpt> <ept> and <it> tags to translation segment
    Unpaired open and close tags are treated as <it>

    :param segment: translation segments
    :return: tagged segment
    """
    tags_stack = []
    open_tags = []
    close_tags = []
    isolated_tags = []
    tag_id = 1
    chunks = tag_re.split(segment)
    for i, chunk in enumerate(chunks):
        open_tag_match = open_tag_re.search(chunk)
        if open_tag_match is not None:
            tag_name = open_tag_match.group(1)
            if tag_name in SELF_CLOSING_TAGS:
                isolated_tags.append((i, tag_id))
                tag_id += 1
                continue
            tags_stack.append((tag_name, i, tag_id))
            tag_id += 1
            continue
        close_tag_match = close_tag_re.search(chunk)
        if close_tag_match is not None:
            tag_name = close_tag_match.group(1)
            # If a closing tag does not have a pair in the stack
            # treat it as an isolated tag.
            open_tag_idx = find_tag(tag_name, tags_stack)
            if open_tag_idx == -1:
                isolated_tags.append((i, tag_id))
                tag_id += 1
                continue
            else:
                open_tags.append((tags_stack[open_tag_idx][1], tags_stack[open_tag_idx][2]))
                close_tags.append((i, tags_stack[open_tag_idx][2]))
                tags_stack.pop(open_tag_idx)
    for item in tags_stack:
        # Add unpaired open tags from the stack to isolated tags.
        isolated_tags.append((item[1], item[2]))
    for tag in open_tags:
        chunks[tag[0]] = '<bpt id="{}">{}</bpt>'.format(
            tag[1], escape(chunks[tag[0]])
        )
    for tag in close_tags:
        chunks[tag[0]] = '<ept id="{}">{}</ept>'.format(
            tag[1], escape(chunks[tag[0]])
        )
    for tag in isolated_tags:
        chunks[tag[0]] = '<it id="{}">{}</it>'.format(
            tag[1], escape(chunks[tag[0]])
        )
    return ''.join(chunks)


def add_xliff_tags(segment):
    # type: (str) -> str
    """
    Add inline XLIFF tags to translatable segment

    :param segment: translatable segment
    :return: segment with HTML tags marked with XLIFF XML tags
    """
    # "XLIFF 1.2 Representation Guide for HTML" strongly recommends to unescape
    # all HTML entities
    return add_t_tags(unescape(segment))
