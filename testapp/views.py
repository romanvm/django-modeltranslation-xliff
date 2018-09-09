# (c) 2018, Roman Miroshnychenko <roman1972@gmail.com>
# License: MIT

from django.views.generic import ListView
from .models import Article


class IndexView(ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'testapp/index.html'
