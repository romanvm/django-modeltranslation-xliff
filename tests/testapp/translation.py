from modeltranslation.translator import register, TranslationOptions
from .models import Article


@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'text')
