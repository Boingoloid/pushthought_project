# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-14 22:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('congress', '0002_auto_20170414_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='congress',
            name='fax',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='congress',
            name='phone',
            field=models.CharField(max_length=20),
        ),
    ]
