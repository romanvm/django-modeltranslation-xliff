Settings
--------

XLIFF Exchange supports the following settings in Django ``settings.py`` file:

- ``XLIFF_EXCHANGE_DISABLE_NLTK``: By default XLIFF Exchange tries to split
  translatable content into translation segments using sentence tokenizer from
  `NLTK`_. Set this settings to ``False`` if you want to disable this feature or if your
  language is not supported. You can find the list of supported languages in
  `nltk_data project`_ on GitHub.
   .. note::
    Without by-sentence segmentation translations segments will include entire
    blocks of text, e.g paragraphs, that can be very big. XLIFF files with such
    big segments are difficult to process with
    :abbr:`CAT (Computer Assisted Translation)` tools. However, some CAT tools
    support additional segmentation of translatable text. Check your CAT program
    options and help to see if your program has such feature.
- ``XLIFF_EXCHANGE_CONTENT_TYPE``: The type of translatable content
  (default: ``'html'``). Currently only ``'html'`` and ``'text'``
  types are supported. Default content type (``'html'``) supports plain text as well,
  but if your content does not include any HTML markup you may want to set
  this settings to ``'text'`` to avoid unnecessary HTML parsing overhead.

.. _NLTK: https://www.nltk.org
.. _nltk_data project: https://github.com/nltk/nltk_data/blob/gh-pages/packages/tokenizers/punkt.xml#L4
