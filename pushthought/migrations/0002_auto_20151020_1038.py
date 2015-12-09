# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pushthought', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='program',
            name='userField',
            field=models.CharField(default=1, max_length=255, blank=True),
        ),
    ]
