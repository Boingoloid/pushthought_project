# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-28 15:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_subscriberemail_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='name_prefix',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='street',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
