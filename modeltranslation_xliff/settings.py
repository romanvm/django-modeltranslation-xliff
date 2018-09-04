from django.conf import settings

#: Disable splitting text into segments with `NLTK <http://www.nltk.org>`_
DISABLE_NLTK = getattr(settings, 'XLIFF_EXCHANGE_DISABLE_NLTK', False)
#: Explicitly set content type. Use "text" if your content has no HTML markup
CONTENT_TYPE = getattr(settings, 'XLIFF_EXCHANGE_CONTENT_TYPE', 'html')
