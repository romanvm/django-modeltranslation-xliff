XLIFF Exchange for django-modeltranslation
==========================================

.. image:: https://travis-ci.org/romanvm/django-modeltranslation-xliff.svg?branch=master
    :target: https://travis-ci.org/romanvm/django-modeltranslation-xliff

**This project is in WIP state and will be released as soon as it's ready!**

This is an extension for `django-modeltranslation`_ package that allows to export
translatable content in `OASIS XLIFF`_ 1.2 format supported by most translation
tools and import content in target languages from translated XLIFF files.

.. figure:: https://raw.githubusercontent.com/romanvm/django-modeltranslation-xliff/master/screenshot.png
  :alt: XLIFF Exchange screenshot

  *Export action and Import form in Django admin*

Introduction
------------

Django has good support for translating UI elements but lacks support for translating
dynamic content stored in a database. There are a number of third-party packages
exist for that purpose, including ``django-modeltranslation`` that uses registration
approach for adding translations to Django model fields. It also provides admin classes
that allow to enter translations for model fields directly in Django admin interface.
However, with large volumes of content and many translation languages such direct
content manipulation can be quite cumbersome. XLIFF Exchange for django-modeltranslation
simplifies translation management by providing an admin action for bulk esporting
translatable content to XLIFF 1.2 format and a form for uploading translated XLIFF
files.

XLIFF 1.2 files are supported bu most (if not all) offline and online translation tools,
including **SDL Trados**, **Deja Vu**, **memoQ**, **Transifex**, **SmartCAT** and many others.
You can simply export your content to XLIFF files, give them to your in-house
translators or external translation contractors to translate, and then import
translated contend back to your Django project. Translatable fields in respective
languages will be updated automatically.

Compatibility
-------------

- Python: 3.4-3.7
- Django: 1.11-2.1
- django-modeltranslation: 0.13-beta1 and above

**Note**: some Python/Django combinations may not work. You can find compatible
combinations in ``tox.ini`` file.

Installation
------------

TBD

Usage
-----

XLIFF Exchange for django-modeltranslation provides ``XliffExchangeMixin`` class
for ``modeltranslation.admin.TranslationAdmin`` that adds XLIFF export/import
functionality.

Minimal example:

.. code-block:: python

  from django.contrib import admin
  from modeltranslation.admin import TranslationAdmin
  from modeltranslation_xliff import XliffExchangeMixin
  from .models import MyModel


  @admin.register(MyModel)
  class MyModelAdmin(XliffExchangeMixin, TranslationAdmin):
      pass

``XliffExchangeMixin`` class is compatible with ``TranslationAdmin`` and its
child classes, e.g. ``TabbedTranslationAdmin``.

XLIFF Exchange for django-modeltranslation conforms to
`XLIFF 1.2 Representation Guide for HTML`_ so it can be used with content
authored with JavaScript WYSIWYG editors that save content in HTML format
such as **TinyMCE** or **CKEditor**.

Settings
--------

XLIFF Exchange supports the following settings in Django ``settings.py`` file:

- ``XLIFF_EXCHANGE_DISABLE_NLTK``: By default XLIFF Exchange tries to split
  translatable content into translation segments using sentence tokenizer from
  `NLTK`_. Set this settings to ``False`` if you want to disable this feature or if your
  language is not supported. You can find the list of supported languages in
  `nltk_data project`_ on GitHub.
- ``XLIFF_EXCHANGE_CONTENT_TYPE``: The type of translatable content
  (default: ``'html'``). Currently only ``'html'`` and ``'text'``
  types are supported. Default content type (``'html'``) supports plain text as well,
  but if you content does not include any HTML markup you may want to set
  this settings to ``'text'`` to avoid unnecessary HTML parsing overhead.

License
-------

MIT. See ``LICENSE.txt``.


.. _django-modeltranslation: https://github.com/deschler/django-modeltranslation
.. _OASIS XLIFF: https://en.wikipedia.org/wiki/XLIFF
.. _NLTK: https://www.nltk.org
.. _nltk_data project: https://github.com/nltk/nltk_data/blob/gh-pages/packages/tokenizers/punkt.xml#L4
.. _XLIFF 1.2 Representation Guide for HTML: http://docs.oasis-open.org/xliff/v1.2/xliff-profile-html/xliff-profile-html-1.2.html
