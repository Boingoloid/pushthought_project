# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-28 19:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20170418_1409'),
    ]

    operations = [
        migrations.AddField(
            model_name='extra',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='extra',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='extra',
            name='prefix',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='extra',
            name='street',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
