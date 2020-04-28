from __future__ import unicode_literals
from django.db import models
from django.contrib import admin


# Create your models here.
class TH_FORM(models.Model):
    timeval=models.CharField(max_length=20)
    temperature = models.IntegerField()
    humidity = models.IntegerField()
