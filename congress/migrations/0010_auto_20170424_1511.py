# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-24 22:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('congress', '0009_remove_congress_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zip',
            name='congress',
        ),
        migrations.AddField(
            model_name='congress',
            name='zip',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='congress.Zip'),
        ),
    ]
