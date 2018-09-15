Usage
=====

XLIFF Exchange for django-modeltranslation provides
:class:`XliffExchangeMixin <modeltranslation_xliff.admin.XliffExchangeMixin>` class
for :class:`modeltranslation.admin.TranslationAdmin` that adds
XLIFF export/import functionality.

Minimal example:

.. code-block:: python

  from django.contrib import admin
  from modeltranslation.admin import TranslationAdmin
  from modeltranslation_xliff import XliffExchangeMixin
  from .models import MyModel


  @admin.register(MyModel)
  class MyModelAdmin(XliffExchangeMixin, TranslationAdmin):
      pass

:class:`XliffExchangeMixin <modeltranslation_xliff.admin.XliffExchangeMixin>` class
is compatible with :class:`modeltranslation.admin.TranslationAdmin` and its
child classes, e.g. :class:`modeltranslation.admin.TabbedTranslationAdmin`.

XLIFF Exchange for django-modeltranslation conforms to
`XLIFF 1.2 Representation Guide for HTML`_ so it can be used with content
authored with JavaScript WYSIWYG editors such as **TinyMCE** or **CKEditor**
that save content in HTML format.

.. note::
  Currently :class:`XliffExchangeMixin <modeltranslation_xliff.admin.XliffExchangeMixin>`
  class is incompatible with customized :class:`ModelAdmin <django.contrib.admin.ModelAdmin>`:
  classes that use custom ``change_list_template`` and ``actions`` class properties.
  As a workaround, you can include the XLIFF file upload form from
  ``modeltranslation_xliff/change_list.html`` template to your custom template
  and/or add ``'export_xliff'`` action to your list of actions.

.. _XLIFF 1.2 Representation Guide for HTML: http://docs.oasis-open.org/xliff/v1.2/xliff-profile-html/xliff-profile-html-1.2.html
