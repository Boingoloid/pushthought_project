# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-24 22:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0008_auto_20170830_1849'),
        ('congress', '0025_auto_20170906_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='congresscounter',
            name='campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='campaigns.Campaign'),
        ),
    ]
