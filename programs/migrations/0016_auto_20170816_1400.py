# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-16 21:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0015_auto_20170815_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='plot_outline',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='program',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
