# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

# Create your models  here.
@python_2_unicode_compatible
class DoubleSyllable(models.Model):
    word = models.CharField(max_length=10)
    classical = models.CharField(max_length=100)
    current = models.CharField(max_length=100)
    sample = models.CharField(max_length=120)
    translation = models.CharField(max_length=200)
    source = models.CharField(max_length=50)
    
    def __str__(self):
        return self.word

class DoubleSyllableTestChoice(models.Model):
    doublesyllable = models.ForeignKey(DoubleSyllable, on_delete=models.CASCADE)
    choice_txt = models.CharField(max_length=100)
    is_correct = models.IntegerField(default=0)

class DoubleSyllableAccess(models.Model):
    doublesyllable = models.ForeignKey(DoubleSyllable, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    access_date = models.DateTimeField('date accessed')

class DoubleSyllableTest(models.Model):
    doublesyllable = models.ForeignKey(DoubleSyllable, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test_date = models.DateTimeField('test accessed')
    test_result = models.IntegerField(default=0)
    test_answer = models.CharField(max_length=100,default="")
