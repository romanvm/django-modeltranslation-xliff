from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from modeltranslation_xliff.admin import XliffExchangeMixin
from .models import Article


@admin.register(Article)
class ArticleAdmin(XliffExchangeMixin, TranslationAdmin):
    pass
