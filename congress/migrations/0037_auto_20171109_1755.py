# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-10 01:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('congress', '0036_auto_20171025_0724'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apiemailfield',
            name='congress',
        ),
        migrations.DeleteModel(
            name='APIEmailField',
        ),
    ]
