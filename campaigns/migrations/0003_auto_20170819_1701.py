# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-20 00:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0002_auto_20170819_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
