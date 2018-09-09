"""
Utility functions for converting model data to XLIFF and back

Currently only HTML content is supported but technically HTML parser can
process plain text as well.
"""
import json
import types
from base64 import b64encode, b64decode
from html import unescape
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _
try:
    from lxml import etree
except ImportError:
    from xml.etree import ElementTree as etree
from .settings import DISABLE_NLTK, CONTENT_TYPE
from . import parsers
from .parsers.segmenter import is_supported_language, segment_text

__all__ = ['create_xliff', 'import_xliff']


def get_content_parser():
    # type: () -> types.ModuleType
    """
    Get parser for a given content type

    :return: content parser instance
    """
    try:
        parser = getattr(parsers, CONTENT_TYPE)
    except AttributeError as ex:
        raise ImproperlyConfigured(
            'Invalid content type: "{}"!'.format(CONTENT_TYPE)
        ) from ex
    return parser


def create_xliff(translation_data):
    # type: (dict) -> str
    """
    Create a XLIFF file from model translation data

    :param translation_data: translation data for Django model objects
    :return: XLIFF file contents
    """
    XML = 'http://www.w3.org/XML/1998/namespace'
    parser = get_content_parser()
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
            content_blocks = parser.parse_content(field['value'])
            for block in content_blocks:
                if (not DISABLE_NLTK and
                        is_supported_language(translation_data['language'])):
                    segments = segment_text(block, translation_data['language'])
                else:
                    segments = (block,)
                for seg in segments:
                    skeleton = skeleton.replace(
                        seg, '%%%{}%%%'.format(segment_id), 1
                    )
                    trans_unit = etree.SubElement(
                        inner_group, 'trans-unit', {
                            'id': str(segment_id),
                            '{{{}}}space'.format(XML): 'preserve'
                        })
                    source = etree.fromstring('<source>{}</source>'.format(
                        parser.add_xliff_tags(seg)
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
        text += get_inner_text(child)
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
