import json
from collections import OrderedDict
from modeltranslation_xliff import utils
from .data import HTML5, TEST_DATA_EN, TEST_DATA_RU, XLIFF_EN, XLIFF_RU


def test_html_parser_html5():
    parser = utils.parser
    parser.feed(HTML5)
    parser.close()
    cont_list = parser.content_list
    assert len(cont_list) == 19
    assert 'HTML5 test sample' in cont_list
    assert 'html5, sample' in cont_list
    assert 'Image caption' in cont_list
    assert 'Paragraph <span class="foo">with</span><em>inline tags</em>.' in cont_list
    assert 'Second line' in cont_list and 'Third line' in cont_list
    assert 'Paragraph with enclosing inline tags.</strong>' in cont_list
    assert 'Paragraph with entity&nbsp;reference.' in cont_list
    assert 'Paragraph with character&#160;reference.' in cont_list
    assert 'Inline image: <img src="http://via.placeholder.com/350x150" />' in cont_list
    assert '.foo { color: blue; }' not in cont_list
    assert 'console.log(\'Hello World!\');' not in cont_list


def test_html_parser_plain_text():
    utils.parser.reset()
    utils.parser.feed('Some plain text.')
    utils.parser.close()
    assert utils.parser.content_list == ['Some plain text.']


def test_add_t_tags():
    string = '<b><i>String with <span>various open</span>,<br>close and isolated tags.</em></b>'
    segment = utils.add_t_tags(string)
    assert segment == '<bpt id="1">&lt;b&gt;</bpt><it id="2">&lt;i&gt;</it>' \
                      'String with <bpt id="3">&lt;span&gt;</bpt>various open' \
                      '<ept id="3">&lt;/span&gt;</ept>,<it id="4">&lt;br&gt;</it>' \
                      'close and isolated tags.<it id="5">&lt;/em&gt;</it>' \
                      '<ept id="1">&lt;/b&gt;</ept>'


def test_create_xliff():
    xliff = utils.create_xliff(TEST_DATA_EN)
    assert xliff == XLIFF_EN


def test_import_xliff():
    translation_data = utils.import_xliff(XLIFF_RU.encode('utf-8'))
    assert translation_data == TEST_DATA_RU
