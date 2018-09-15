Translating XLIFF Files
=======================

XLIFF Exchange creates XLIFF 1.2 files compatible with `OASIS specification`_.
Such files are supported by various offline and online
:abbr:`CAT (Computer Assisted Translation)` tools, including **SDL Trados**,
**Deja Vu**, **memoQ**, **Transifex**, **SmartCAT** and many others,
so you can easily outsource translation to external providers or organize your
own workspace on translation portals like **Transifex** or **SmartCAT**.

Translation Workflow
--------------------

Example translation workflow with ``django-modeltranslation`` and XLIFF Exchange
is described below:

- You select models that need to be translated, import their content to
  XLIFF file(s) and then give imported XLIFF files to your in-house translators
  or external translation contractors.
- The translators translate those XLIFF files using their favorite CAT tools
  and return you translated XLIFF files.
- You import translated XLIFF files to your Django application. Translatable
  fields in respective language(s) will be updated automatically.

Important Notes
---------------

- XLIFF Exchange does not accept partially translated XLIFF files, that is,
  files with missing target translations.
- Some translation tools allow to create "intermediary" XLIFF files for exchanging
  translations with other tools. XLIFF Exchange does not support such files.
  Translations needs to be saved as "target" XLIFF files that contain all necessary
  metadata for importing translations back to your Django project.
- Translated XLIFF files must have the target language defined, otherwise
  XLIFF Exchange won't know which language to update. Check import/export options
  for XLIFF 1.2 files in your CAT program settings. For example, if you are using
  **SDL Trados Studio**, go to
  :menuselection:`File --> Options --> File Types --> XLIFF --> Settings` and check
  :guilabel:`Overwrite target-language attribute when generating translated file`
  option before importing XLIFF files to Trados Studio.

.. figure:: _static/Trados.XLIFF.settings.png
  :alt: SDL Trados XLIFF Settings

  *XLIFF 1.2 import/export settings in SDL Trados Studio*

.. _OASIS specification: http://docs.oasis-open.org/xliff/xliff-core/xliff-core.html
