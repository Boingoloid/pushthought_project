# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-18 21:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='extra',
            name='zip',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='extra',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
