# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-19 00:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0004_auto_20170418_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='imdb',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
