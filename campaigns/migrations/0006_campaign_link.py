# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-21 00:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0005_campaign_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
