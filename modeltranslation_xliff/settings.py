from django.conf import settings

DISABLE_NLTK = getattr(settings, 'XLIFF_EXCHANGE_DISABLE_NLTK', False)
