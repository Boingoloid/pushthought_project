# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-24 22:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0008_auto_20170830_1849'),
        ('actions', '0011_auto_20170917_2041'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actions', to='campaigns.Campaign'),
        ),
    ]
