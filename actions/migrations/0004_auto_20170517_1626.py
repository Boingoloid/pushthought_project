# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-17 23:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0003_auto_20170517_1558'),
    ]

    operations = [
        migrations.RenameField(
            model_name='action',
            old_name='receiver',
            new_name='congress',
        ),
    ]
