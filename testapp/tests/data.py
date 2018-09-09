import json
from collections import OrderedDict

HTML5 = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta description="HTML5 test sample">
    <meta keywords="html5, sample">
    <meta http-equiv="keywords" content="sample, html5" />

    <title>This is title</title>

    <style>.foo { color: blue; }</style>
    <script>console.log('Hello World!');</script>
</head>
<body>
    <h1>This is header</h1>
    <img src="http://via.placeholder.com/350x150" alt="Image caption">
    <p>Simple paragraph.</p>
    <p>
        Multiline paragraph<br>
        Second line<br />
        Third line
    </p>
    <p>Paragraph <span class="foo">with</span> <em>inline tags</em>.</p>
    <p>Paragraph <a href="http://example.com">with a link</a>.</p>
    <p><strong>Paragraph with enclosing inline tags.</strong></p>
    <p>&quot;Paragraph with entity&nbsp;references.&quot;</p>
    <p>Paragraph with character&#160;reference.</p>
    <p>First sentence. Second sentence. Third sentence</p>
    <p>Inline image: <img src="http://via.placeholder.com/350x150" /></p>
    <pre><code>import this</code></pre>
</body>
</html>'''

_TEST_DATA_EN = '''{
    "name": "Article",
    "language": "en-us",
    "objects": [{
        "id": "1",
        "fields": [
            {"name": "title", "value": "Plain Text"},
            {"name": "text",
             "value": "A piece of plain text. The second sentence."}
        ]}, {
        "id": "2",
        "fields": [
            {"name": "title", "value": "Rich Text"},
            {"name": "text",
             "value": "<p>A piece of rich text with HTML tags. The <strong>second sentence</strong>. The <em>third sentence</em>.</p>"}
        ]
    }]
}'''

# This is needed for testing in Py3.5 and 3.6+ with different dict behavior
TEST_DATA_EN = json.loads(_TEST_DATA_EN, object_pairs_hook=OrderedDict)

XLIFF_EN = '<xliff version="1.2">' \
        '<file datatype="database" original="Article" source-language="en-us">' \
        '<header>' \
        '<tool tool-id="django-modeltranslation-xliff" tool-name="XLIFF Exchange for django-modeltranslation"/>' \
        '<skl>' \
        '<internal-file form="base64">eyJuYW1lIjogIkFydGljbGUiLCAibGFuZ3VhZ2UiOiAiZW4tdXMiLCAib2JqZWN0cyI6IFt7ImlkIjogIjEiLCAiZmllbGRzIjogW3sibmFtZSI6ICJ0aXRsZSIsICJ2YWx1ZSI6ICIlJSUxJSUlIn0sIHsibmFtZSI6ICJ0ZXh0IiwgInZhbHVlIjogIiUlJTIlJSUgJSUlMyUlJSJ9XX0sIHsiaWQiOiAiMiIsICJmaWVsZHMiOiBbeyJuYW1lIjogInRpdGxlIiwgInZhbHVlIjogIiUlJTQlJSUifSwgeyJuYW1lIjogInRleHQiLCAidmFsdWUiOiAiPHA+JSUlNSUlJSAlJSU2JSUlICUlJTclJSU8L3A+In1dfV19</internal-file>' \
        '</skl></header>' \
        '<body>' \
        '<group id="1" resname="Article" restype="x-django-model">' \
        '<group resname="title" restype="x-django-model-field">' \
        '<trans-unit id="1" xml:space="preserve">' \
        '<source>Plain Text</source></trans-unit></group>' \
        '<group resname="text" restype="x-django-model-field">' \
        '<trans-unit id="2" xml:space="preserve">' \
        '<source>A piece of plain text.</source></trans-unit>' \
        '<trans-unit id="3" xml:space="preserve">' \
        '<source>The second sentence.</source></trans-unit>' \
        '</group></group>' \
        '<group id="2" resname="Article" restype="x-django-model">' \
        '<group resname="title" restype="x-django-model-field">' \
        '<trans-unit id="4" xml:space="preserve">' \
        '<source>Rich Text</source>' \
        '</trans-unit></group>' \
        '<group resname="text" restype="x-django-model-field">' \
        '<trans-unit id="5" xml:space="preserve">' \
        '<source>A piece of rich text with HTML tags.</source></trans-unit>' \
        '<trans-unit id="6" xml:space="preserve">' \
        '<source>The <bpt id="1">&lt;strong&gt;</bpt>second sentence<ept id="1">&lt;/strong&gt;</ept>.</source></trans-unit>' \
        '<trans-unit id="7" xml:space="preserve">' \
        '<source>The <bpt id="1">&lt;em&gt;</bpt>third sentence<ept id="1">&lt;/em&gt;</ept>.</source></trans-unit>' \
        '</group></group></body></file></xliff>'


XLIFF_RU = '<?xml version="1.0" encoding="utf-8"?>' \
           '<xliff version="1.2">' \
           '<file datatype="database" original="Article" source-language="en-us" target-language="ru-RU">' \
           '<header>' \
           '<tool tool-id="django-modeltranslation-xliff" tool-name="XLIFF Exchange for django-modeltranslation" />' \
           '<skl>' \
           '<internal-file form="base64">eyJuYW1lIjogIkFydGljbGUiLCAibGFuZ3VhZ2UiOiAiZW4tdXMiLCAib2JqZWN0cyI6IFt7ImlkIjogIjEiLCAiZmllbGRzIjogW3sibmFtZSI6ICJ0aXRsZSIsICJ2YWx1ZSI6ICIlJSUxJSUlIn0sIHsibmFtZSI6ICJ0ZXh0IiwgInZhbHVlIjogIiUlJTIlJSUgJSUlMyUlJSJ9XX0sIHsiaWQiOiAiMiIsICJmaWVsZHMiOiBbeyJuYW1lIjogInRpdGxlIiwgInZhbHVlIjogIiUlJTQlJSUifSwgeyJuYW1lIjogInRleHQiLCAidmFsdWUiOiAiPHA+JSUlNSUlJSAlJSU2JSUlICUlJTclJSU8L3A+In1dfV19</internal-file>' \
           '</skl></header>' \
           '<body>' \
           '<group id="1" resname="Article" restype="x-django-model">' \
           '<group resname="title" restype="x-django-model-field">' \
           '<trans-unit id="1" xml:space="preserve">' \
           '<source>Plain Text</source>' \
           '<target>Простой текст</target></trans-unit></group>' \
           '<group resname="text" restype="x-django-model-field">' \
           '<trans-unit id="2" xml:space="preserve">' \
           '<source>A piece of plain text.</source>' \
           '<target>Фрагмент простого текста.</target></trans-unit>' \
           '<trans-unit id="3" xml:space="preserve">' \
           '<source>The second sentence.</source>' \
           '<target>Второе предложение.</target></trans-unit></group>' \
           '</group><group id="2" resname="Article" restype="x-django-model">' \
           '<group resname="title" restype="x-django-model-field">' \
           '<trans-unit id="4" xml:space="preserve">' \
           '<source>Rich Text</source>' \
           '<target>Форматированный тест</target></trans-unit>' \
           '</group><group resname="text" restype="x-django-model-field">' \
           '<trans-unit id="5" xml:space="preserve">' \
           '<source>A piece of rich text with HTML tags.</source>' \
           '<target>Фрагмент форматированного текста с тегами HTML.</target></trans-unit>' \
           '<trans-unit id="6" xml:space="preserve">' \
           '<source>The <bpt id="1">&lt;strong&gt;</bpt>second sentence<ept id="1">&lt;/strong&gt;</ept>.</source>' \
           '<target>Второе <bpt id="1">&lt;strong&gt;</bpt>предложение<ept id="1">&lt;/strong&gt;</ept>.</target></trans-unit>' \
           '<trans-unit id="7" xml:space="preserve">' \
           '<source>The <bpt id="1">&lt;em&gt;</bpt>third sentence<ept id="1">&lt;/em&gt;</ept>.</source>' \
           '<target>Третье <bpt id="1">&lt;em&gt;</bpt>предложение<ept id="1">&lt;/em&gt;</ept>.</target>' \
           '</trans-unit></group></group>' \
           '</body></file></xliff>'

TEST_DATA_RU = {
    'name': 'Article',
    'language': 'ru-ru',
    'objects': [
        {'id': '1',
         'fields': [
            {'name': 'title', 'value': 'Простой текст'},
            {'name': 'text', 'value': 'Фрагмент простого текста. '
                                      'Второе предложение.'}
          ]},
        {'id': '2',
         'fields': [
             {'name': 'title', 'value': 'Форматированный тест'},
             {'name': 'text',
              'value': '<p>Фрагмент форматированного текста с '
                       'тегами HTML. Второе '
                       '<strong>предложение</strong>. Третье '
                       '<em>предложение</em>.</p>'}
          ]}
    ]
}
