# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-18 17:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hashtag', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hashtagcounter',
            name='program',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='programs.Program'),
        ),
    ]
