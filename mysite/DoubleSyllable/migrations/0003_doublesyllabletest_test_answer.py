# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-30 07:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DoubleSyllable', '0002_doublesyllabletestchoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='doublesyllabletest',
            name='test_answer',
            field=models.CharField(default='', max_length=100),
        ),
    ]
