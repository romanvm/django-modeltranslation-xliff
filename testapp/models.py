from django.db import models
from tinymce import HTMLField


class Article(models.Model):
    title = models.CharField(max_length=255)
    text = HTMLField()

    class Meta:
        ordering = ['pk']
