# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-13 14:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0012_action_campaign'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='is_sent',
            field=models.NullBooleanField(),
        ),
    ]
