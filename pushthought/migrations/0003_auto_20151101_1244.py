# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pushthought', '0002_auto_20151020_1038'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocalRepresentative',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='category',
            field=models.CharField(max_length=255),
        ),
    ]
