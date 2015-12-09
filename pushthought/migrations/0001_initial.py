# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=255, choices=[(b'Local Representative', b'Local Representative'), (b'Regulator', b'Regulator'), (b'Executive', b'Executive'), (b'Corporation', b'Corporation'), (b'Petition', b'Petition'), (b'Donation', b'Donation'), (b'Other', b'Other')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(default=0)),
                ('image', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('isMessage', models.NullBooleanField()),
                ('messageText', models.TextField(null=True, blank=True)),
                ('messageType', models.CharField(max_length=255, null=True, blank=True)),
                ('targetName', models.CharField(max_length=255, null=True, blank=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, blank=True)),
                ('twitterID', models.CharField(max_length=255, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('website', models.URLField(null=True, blank=True)),
                ('facebook_page', models.URLField(null=True, blank=True)),
            ],
            options={
                'ordering': ['category', '-isMessage', 'order'],
            },
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=255)),
                ('image', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('date_released', models.DateField()),
                ('title', models.CharField(max_length=255)),
                ('image', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('link', models.URLField()),
                ('description', models.TextField()),
                ('episode', models.CharField(max_length=255, null=True, blank=True)),
                ('program', models.ForeignKey(editable=False, to='pushthought.Program')),
            ],
            options={
                'ordering': ['-date_released'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('website', models.URLField(blank=True)),
                ('picture', models.ImageField(upload_to=b'profile_images', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='menuitem',
            name='segment',
            field=models.ForeignKey(to='pushthought.Segment'),
        ),
    ]
