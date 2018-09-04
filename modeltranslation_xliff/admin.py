import logging
from collections import OrderedDict
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Model, QuerySet
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect, \
    HttpResponseNotAllowed
from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from modeltranslation.fields import TranslationField
from modeltranslation.settings import DEFAULT_LANGUAGE, AVAILABLE_LANGUAGES
from .utils import create_xliff, import_xliff


class XliffExchangeMixin:
    """
    XLIFF exchange for django-modeltranslation

    This mixin adds a custom admin action for exporting translatable content
    to XLIFF format and a file upload form for importing translations
    from translated XLIFF files.

    Usage example::

        from django.contrib import admin
        from modeltranslation.admin import TranslationAdmin
        from modeltranslation_xliff.admin import XliffExchangeMixin
        from .models import MyModel


        @admin.register(MyModel)
        class MyModelAdmin(XliffExchangeMixin, TranslationAdmin):
            pass
    """
    change_list_template = 'modeltranslation_xliff/change_list.html'
    actions = ['export_xliff']

    @staticmethod
    def _get_object_trans_source(obj):
        # type: (Model) -> dict
        """
        Extract translatable content from a model object

        :param obj: Django model object
        :return: dictionary with translatable content
        """
        fields = obj._meta.get_fields()
        translatable_fields = []
        for f in fields:
            name, *lang = f.name.split('_', 1)
            # .replace('ind', 'id') fixes Indonesian langugage code
            lang = lang[0].replace('_', '-').replace('ind', 'id') if lang else ''
            if isinstance(f, TranslationField) and lang == DEFAULT_LANGUAGE:
                # OrderedDict is used to mitigate different dict behavior
                # in Py3.5 and Py3.6+ where dict key order is preserved.
                # This is needed to pass tests on all Python versions.
                f_dict = OrderedDict()
                f_dict['name'] = name
                f_dict['value'] = getattr(obj, f.name)
                translatable_fields.append(f_dict)
        obj_dict = OrderedDict()
        obj_dict['id'] = str(obj.pk)
        obj_dict['fields'] = translatable_fields
        return obj_dict

    def _get_model_trans_source(self, queryset):
        # type: (QuerySet) -> dict
        """
        Extract translatable content from a queryset

        :param queryset: queryset for model objects to translate
        :return: dictionary with translatable content
        """
        translatable_objects = []
        for obj in queryset:
            translatable_objects.append(self._get_object_trans_source(obj))
        model_dict = OrderedDict()
        model_dict['name'] = self.model.__name__
        model_dict['language'] = DEFAULT_LANGUAGE
        model_dict['objects'] = translatable_objects
        return model_dict

    @staticmethod
    def _get_language_code(language):
        # type: (str) -> str
        """
        Get actual language code for translated content

        :param language: language code from a translated XLIFF
        :return: actual language code from Django project settings
        """
        if language in AVAILABLE_LANGUAGES:
            # Language codes match, we are good.
            return language
        for lang in AVAILABLE_LANGUAGES:
            # Try to find matching language without a country code
            if language[:2] == lang[:2]:
                return lang
        raise ValidationError(
            _('Unknown translation language: "{}"!').format(language)
        )

    def _update_translations(self, translation_data):
        # type: (dict) -> None
        """
        Update translatable models content from imported XLIFF

        :param translation_data: imported translations from a XLIFF
        """
        if translation_data['name'] != self.model.__name__:
            raise ValidationError(
                _('Uploaded XLIFF is for different model: "{}"!').format(
                    translation_data['name']
                )
            )
        language = self._get_language_code(
            translation_data['language']
        ).replace('-', '_')
        object_pks = (int(obj['id']) for obj in translation_data['objects'])
        queryset = self.model.objects.filter(pk__in=object_pks)
        fields = [f['name'] + '_' + language
                  for f in translation_data['objects'][0]['fields']]
        for item, obj in zip(queryset, translation_data['objects']):
            for i, field in enumerate(obj['fields']):
                setattr(item, fields[i], field['value'])
                item.save(update_fields=fields)

    def export_xliff(self, request, queryset):
        # type: (HttpRequest, QuerySet) -> HttpResponse
        """
        Export XLIFF view

        :param request: request instance.
        :param queryset: a queryset for model objects to translate.
        :return: response containing a XLIFF file with content to translate
        """
        response = HttpResponse(
            create_xliff(self._get_model_trans_source(queryset)).encode('utf-8')
        )
        response['Content-Type'] = 'application/x-xliff-xml'
        response['Content-Disposition'] = \
            'attachment; filename="{}.xlf"'.format(self.model.__name__.lower())
        return response

    export_xliff.short_description = _('Export to XLIFF')

    def get_urls(self):
        # type: () -> list
        urls = [
            url(r'import-xliff/$', self.import_xliff, name='import_xliff')
        ] + super().get_urls()
        return urls

    def import_xliff(self, request):
        # type: (HttpRequest) -> HttpResponse
        """
        Import XLIFF view

        :param request: request instance
        :return: redirect response
        """
        if request.method != 'POST':
            return HttpResponseNotAllowed('POST')
        try:
            fo = request.FILES.get('_upload-xliff')
            if not fo:
                raise ValidationError(_('No XLIFF file uploaded!'))
            xliff = fo.read()
            translation_data = import_xliff(xliff)
            self._update_translations(translation_data)
        except ValidationError as ex:
            self.message_user(request, ex.message, level=messages.ERROR)
        except Exception as ex:
            logging.exception('Error while importing XLIFF!')
            self.message_user(
                request,
                _('Unexpected error while importing XLIFF: {}').format(str(ex)),
                level=messages.ERROR
            )
        else:
            self.message_user(
                request,
                _('Translation for "{}" was imported successfully.'.format(
                    translation_data['language']
                ))
            )
        return HttpResponseRedirect('../')
