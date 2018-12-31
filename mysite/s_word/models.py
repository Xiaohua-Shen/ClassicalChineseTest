# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
@python_2_unicode_compatible 
class SWord(models.Model):
    sword = models.CharField(max_length=4)
    pinyin = models.CharField(max_length=4,default="")
    word_class = models.CharField(max_length=10)
    meaning = models.CharField(max_length=100)
    sample = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    translation = models.CharField(max_length=100)

    def __str__(self):
        return self.sword

class SWordTest1Choice(models.Model):
    sword = models.ForeignKey(SWord, on_delete=models.CASCADE)
    test_type = models.CharField(max_length=10)
    choice_txt = models.CharField(max_length=100)
    is_correct = models.IntegerField(default=0)
