# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-07 20:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20170928_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='twitter',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
