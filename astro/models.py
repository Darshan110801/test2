from django.db import models
from datetime import datetime


class Prev30(models.Model):
    date = models.CharField(max_length=11, default='')
    url = models.TextField(default='')
    explanation = models.TextField(default='')
    title = models.TextField(default='')


class Astronomer(models.Model):
    name = models.CharField(max_length=1000, default='')
    image_link = models.TextField(default='')
    yob = models.CharField(default='', max_length=5)
    yod = models.CharField(default='', max_length=5)
    books = models.JSONField(default='')
    summary = models.TextField(default='')
    wiki_link = models.TextField(default='')
