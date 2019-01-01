# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
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

# word related question count
class SWordQuestionByWord(models.Model):
    sword = models.CharField(max_length=100)
    questioncount = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = "v_swordtestquestion_count"

# user passed word count
class SWordUserQuestionByWord(models.Model):
    sword = models.CharField(max_length=100)
    questioncount = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    passedcount = models.IntegerField(default=0)
    status = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "v_user_passed_question_count"

class SWordTest(models.Model):
    sword = models.ForeignKey(SWord, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test_date = models.DateTimeField('test accessed')
    test_result = models.IntegerField(default=0)
    test_answer = models.CharField(max_length=100,default="")
    test_type = models.CharField(max_length=10)