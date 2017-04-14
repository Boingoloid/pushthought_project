# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-14 21:50
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Congress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('first_name', models.CharField(max_length=30)),
                ('middle_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('state_name', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=5)),
                ('oc_email', models.EmailField(max_length=254)),
                ('title', models.CharField(max_length=20)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('fax', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('twitter_id', models.CharField(max_length=30)),
                ('bioguide_id', models.CharField(max_length=30)),
                ('image', models.ImageField(blank=True, null=True, upload_to=b'')),
                ('office', models.CharField(max_length=100)),
                ('thomas_id', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('senate_class', models.IntegerField()),
                ('term_end', models.DateField()),
                ('crp_id', models.CharField(max_length=50)),
                ('party', models.CharField(max_length=1)),
                ('votesmart_id', models.IntegerField()),
                ('website', models.URLField()),
                ('lis_id', models.CharField(max_length=100)),
                ('leadership_role', models.CharField(max_length=100)),
                ('govtrack_id', models.CharField(max_length=100)),
                ('facebook_id', models.CharField(max_length=100)),
                ('birthday', models.DateField()),
                ('term_start', models.DateField()),
                ('nickname', models.CharField(max_length=100)),
                ('contact_form', models.URLField()),
                ('ocd_id', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=1)),
                ('name_suffix', models.CharField(max_length=100)),
                ('chamber', models.CharField(max_length=100)),
                ('state_rank', models.CharField(max_length=100)),
                ('fec_ids', models.TextField()),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
        migrations.CreateModel(
            name='Zip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('code', models.IntegerField()),
                ('congress', models.ManyToManyField(to='congress.Congress')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
    ]
