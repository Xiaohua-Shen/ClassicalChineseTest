# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models

# Register your models here.
from .models import SWord,SWordTest1Choice

class ChoiceInline(admin.TabularInline):
    model = SWordTest1Choice
    extra = 3

class SWordAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }
    fieldsets = [
        ('实词',               {'fields': ['sword']}),
        ('释义', {'fields': ['pinyin', 'word_class', 'meaning']}),
        ('例句', {'fields': ['source', 'sample', 'translation']}),
    ]
    list_display = ('sword', 'word_class', 'pinyin', 'meaning','sample','source')
    search_fields = ['sword']
    inlines = [ChoiceInline]

admin.site.register(SWord, SWordAdmin)
