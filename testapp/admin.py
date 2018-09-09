from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from modeltranslation_xliff import XliffExchangeMixin
from .models import Article


@admin.register(Article)
class ArticleAdmin(XliffExchangeMixin, TabbedTranslationAdmin):
    list_display = ('title',)
