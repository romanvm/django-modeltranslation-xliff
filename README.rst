XLIFF Exchange for django-modeltranslation
==========================================

.. image:: https://travis-ci.org/romanvm/django-modeltranslation-xliff.svg?branch=master
  :target: https://travis-ci.org/romanvm/django-modeltranslation-xliff
.. image:: https://codecov.io/gh/romanvm/django-modeltranslation-xliff/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/romanvm/django-modeltranslation-xliff

XLIFF Exchange is an extension for `django-modeltranslation`_ package that allows to export
translatable content in `OASIS XLIFF`_ 1.2 format supported by most translation
tools and import content in target languages from translated XLIFF files.

.. figure:: https://raw.githubusercontent.com/romanvm/django-modeltranslation-xliff/master/screenshot.png
  :alt: XLIFF Exchange screenshot

  *Export action and Import form in Django admin*

Introduction
------------

Django has good support for translating UI elements but lacks support for translating
dynamic content stored in a database. There are a number of third-party packages
for that purpose, including ``django-modeltranslation`` that uses registration
approach for adding translations to Django model fields. It also provides admin classes
that allow to enter translations for model fields directly in Django admin interface.
However, with large volumes of content and many translation languages such direct
content manipulation can be quite cumbersome. XLIFF Exchange for django-modeltranslation
simplifies translation management by providing an admin action for bulk exporting
translatable content to XLIFF 1.2 format and a form for uploading translated XLIFF
files.

XLIFF 1.2 files are supported bu most (if not all) offline and online translation tools,
including **SDL Trados**, **Deja Vu**, **memoQ**, **Transifex**, **SmartCAT** and many others.
You can simply export your content to XLIFF files, give them to your in-house
or external translators to translate, and then import translated contend back
to your Django project. Translatable fields in respective languages
will be updated automatically.

Compatibility
-------------

- Python: 3.4-3.7
- Django: 1.11-2.1
- django-modeltranslation: 0.13-beta1 and above

**Note**: some Python/Django combinations may not work. You can find compatible
combinations in ``tox.ini`` file.

Installation
------------

- Install XLIFF Exchange with ``pip``::

    pip install django-modeltranslation-xliff

- Add ``'modeltranslation_xliff'`` to ``INSTALLED_APPS`` in your project's
  ``settings.py``:

.. code-block:: python

    INSTALLED_APPS = (
        'modeltranslation',
        'modeltranslation_xliff',
        ...
    )

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

Documentation
-------------

See `XLIFF Exchange documentation`_ for more info.

License
-------

MIT. See ``LICENSE.txt``.

.. _django-modeltranslation: https://github.com/deschler/django-modeltranslation
.. _OASIS XLIFF: https://en.wikipedia.org/wiki/XLIFF
.. _XLIFF Exchange documentation: https://romanvm.github.io/django-modeltranslation-xliff

