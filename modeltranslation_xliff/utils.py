"""
Utility functions for converting model data to XLIFF and back

The module includes HTML parser for parsing content with HTML tags.
"""
import json
import logging
import re
import types
from base64 import b64encode, b64decode
from html import escape, unescape
from html.parser import HTMLParser
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
try:
    from lxml import etree
except ImportError:
    from xml.etree import ElementTree as etree
from .settings import DISABLE_NLTK

if not DISABLE_NLTK:
    from nltk import download
    from nltk.tokenize import sent_tokenize
    try:
        sent_tokenize('Test.')
    except LookupError:
        download('punkt')

__all__ = ['create_xliff', 'import_xliff']

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
        if self._current_block:
            self._current_block += '&#' + name + ';'

    def handle_entityref(self, name):
        if self._current_block:
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


parser = ContentParser()


def segment_html(html, lang_code):
    # type: (str, str) -> types.GeneratorType
    """
    Extract translatable segments from a HTML document

    :param html: HTML document
    :param lang_code: language code
    :return: generator of translatable segments
    """
    language = NLTK_SUPPORTED_LANGUAGES.get(lang_code[:2])
    parser.reset()
    parser.feed(html)
    parser.close()
    for item in parser.content_list:
        # Skip <pre><code> blocks
        if pre_code_re.search(item) is None:
            if not DISABLE_NLTK and language:
                for segment in sent_tokenize(item, language):
                    if not tag_string_re.search(segment):
                        yield segment
            else:
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


def create_xliff(translation_data):
    # type: (dict) -> str
    """
    Create a XLIFF file from model translation data

    :param translation_data: translation data for Django model objects
    :return: XLIFF file contents
    """
    XML = 'http://www.w3.org/XML/1998/namespace'
    xliff = etree.Element('xliff', {'version': '1.2'}, nsmap={'xml': XML})
    file = etree.SubElement(xliff, 'file', {
        'original': translation_data['name'],
        'datatype': 'database',
        'source-language': translation_data['language']
    })
    header = etree.SubElement(file, 'header')
    etree.SubElement(header, 'tool', {
        'tool-id': 'django-modeltranslation-xliff',
        'tool-name': 'XLIFF Exchange for django-modeltranslation'
    })
    skl = etree.SubElement(header, 'skl')
    internal_file = etree.SubElement(skl, 'internal-file', {'form': 'base64'})
    skeleton = json.dumps(translation_data)
    body = etree.SubElement(file, 'body')
    segment_id = 1
    for obj in translation_data['objects']:
        outer_group = etree.SubElement(
            body, 'group', {
                'id': obj['id'],
                'restype': 'x-django-model',
                'resname': translation_data['name']
            })
        for field in obj['fields']:
            inner_group = etree.SubElement(
                outer_group, 'group', {
                    'restype': 'x-django-model-field',
                    'resname': field['name']
                })
            for seg in segment_html(field['value'], translation_data['language']):
                skeleton = skeleton.replace(seg, '%%%{}%%%'.format(segment_id), 1)
                trans_unit = etree.SubElement(
                    inner_group, 'trans-unit', {
                        'id': str(segment_id),
                        '{{{}}}space'.format(XML): 'preserve'
                    })
                source = etree.fromstring('<source>{}</source>'.format(
                    add_t_tags(unescape(seg))
                ))
                trans_unit.append(source)
                segment_id += 1
        internal_file.text = b64encode(skeleton.encode('utf-8')).decode('ascii')
    return etree.tostring(etree.ElementTree(xliff), encoding='unicode')


def get_inner_text(elem):
    # type: (etree.Element) -> str
    """
    Extract Element's inner content as a string

    :param elem: :class:`Element <xml.etree.ElementTree.Element>`
    :return: Element's content
    """
    text = unescape(elem.text or '')
    for child in list(elem):
        text += unescape(get_inner_text(child))
    text += unescape(elem.tail or '')
    return text


def import_xliff(xliff):
    # type: (bytes) -> dict
    """
    Extract translation data from a translated XLIFF file

    :param xliff: XLIFF file as :class:`bytes` string
    :return: translation data
    """
    xliff_elem = etree.fromstring(xliff)
    tool = xliff_elem.find('./file/header/tool')
    # Basic sanity check
    if tool is None or tool.attrib.get('tool-id') != 'django-modeltranslation-xliff':
        raise ValidationError('Invalid XLIFF file!')
    file = xliff_elem.find('file')
    target_language = file.attrib.get('target-language')
    if not target_language:
        raise ValidationError(_('The XLIFF file has no target language defined!'))
    target_language = target_language.lower().replace('_', '-')
    internal_file = file.find('./header/skl/internal-file[@form="base64"]')
    if internal_file is None:
        raise ValidationError(_('Invalid XLIFF file!'))
    skeleton = b64decode(internal_file.text.encode('ascii')).decode('utf-8')
    trans_units = file.findall('.//trans-unit')
    for tu in trans_units:
        segment_id = tu.attrib.get('id')
        if not segment_id:
            raise ValidationError(_('Invalid XLIFF file!'))
        target = tu.find('target')
        if target is None:
            raise ValidationError(
                _('Missing translation for segment #{}!').format(segment_id)
            )
        translation = get_inner_text(target)
        skeleton = skeleton.replace('%%%{}%%%'.format(segment_id), translation, 1)
    translation_data = json.loads(skeleton)
    translation_data['language'] = target_language
    return translation_data
