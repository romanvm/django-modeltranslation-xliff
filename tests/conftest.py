import pytest
from .testapp.models import Article


@pytest.fixture
def populate_db(django_db_blocker):
    with django_db_blocker.unblock():
        a1 = Article(
            title='Plain Text',
            text='A piece of plain text. The second sentence.'
        )
        a1.save()
        a2 = Article(
            title='Rich Text',
            text='<p>A piece of rich text with HTML tags. '
                 'The <strong>second sentence</strong>. '
                 'The <em>third sentence</em>.</p>'
        )
        a2.save()
