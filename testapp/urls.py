from django.contrib import admin
from django.conf.urls import url, include
from .views import IndexView


urlpatterns = [
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name='index')
]
