# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-27 23:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('congress', '0017_auto_20170527_1630'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='field',
            name='congress',
        ),
        migrations.DeleteModel(
            name='Field',
        ),
    ]
