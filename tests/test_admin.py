from io import BytesIO
from unittest import mock
import pytest
from django.contrib.messages import INFO, ERROR
from django.urls import reverse
from .testapp.admin import ArticleAdmin
from .testapp.models import Article
from .data import XLIFF_EN, XLIFF_RU, TEST_DATA_RU


def catch_error_message(_, msg, level=INFO):
    if level == ERROR:
        raise AssertionError('Test for uploading XLIFF failed: {}'.format(msg))


@pytest.mark.usefixtures('populate_db')
def test_export_xliff(admin_client):
    data = {
        'action': 'export_xliff',
        '_selected_action': [str(obj.pk) for obj in Article.objects.all()]
    }
    response = admin_client.post(reverse('admin:testapp_article_changelist'),
                                 data=data)
    assert response.content == XLIFF_EN.encode('utf-8')


@pytest.mark.usefixtures('populate_db')
@mock.patch.object(ArticleAdmin, 'message_user', side_effect=catch_error_message)
def test_import_xliff(_, admin_client):
    data = {'_upload-xliff': BytesIO(XLIFF_RU.encode('utf-8'))}
    response = admin_client.post(reverse('admin:import_xliff'), data=data)
    assert response.status_code == 302
    article = Article.objects.get(pk=1)
    assert getattr(article, 'title_ru_ru') == TEST_DATA_RU['objects'][0]['fields'][0]['value']
    assert getattr(article, 'text_ru_ru') == TEST_DATA_RU['objects'][0]['fields'][1]['value']


@mock.patch.object(ArticleAdmin, 'message_user', side_effect=catch_error_message)
def test_import_xliff_no_file(_, admin_client):
    with pytest.raises(AssertionError):
        admin_client.post(reverse('admin:import_xliff'), data={})


@mock.patch.object(ArticleAdmin, 'message_user', side_effect=catch_error_message)
def test_import_xliff_empty_file(_, admin_client):
    with pytest.raises(AssertionError):
        admin_client.post(reverse('admin:import_xliff'),
                          data={'_upload-xliff': BytesIO()})


def test_import_xliff_ivalid_method(admin_client):
    response = admin_client.get(reverse('admin:import_xliff'))
    assert response.status_code == 405
