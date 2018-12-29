# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models

# Register your models here.
from .models import DoubleSyllable,DoubleSyllableTestChoice

class ChoiceInline(admin.TabularInline):
    model = DoubleSyllableTestChoice
    extra = 3

class DoubleSyllableAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }
    fieldsets = [
        ('双音词',               {'fields': ['word']}),
        ('古今异义', {'fields': ['classical', 'current']}),
        ('例句', {'fields': ['source', 'sample', 'translation']}),
    ]
    list_display = ('word', 'classical','current','sample','source')
    search_fields = ['word']
    inlines = [ChoiceInline]

admin.site.register(DoubleSyllable, DoubleSyllableAdmin)
