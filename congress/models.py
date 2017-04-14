from __future__ import unicode_literals

from phonenumber_field.modelfields import PhoneNumberField

from django.db import models
from django_extensions.db.models import TimeStampedModel


class Zip(TimeStampedModel):
    code = models.IntegerField()
    congress = models.ManyToManyField('Congress')


class Congress(TimeStampedModel):
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    state_name = models.CharField(max_length=30)
    state = models.CharField(max_length=5)
    oc_email = models.EmailField()
    title = models.CharField(max_length=20)
    phone = PhoneNumberField()
    fax = PhoneNumberField()
    twitter_id = models.CharField(max_length=30)
    bioguide_id = models.CharField(max_length=30)
    image = models.ImageField(blank=True, null=True)
    office = models.CharField(max_length=100)
    thomas_id = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    senate_class = models.IntegerField()
    term_end = models.DateField()
    crp_id = models.CharField(max_length=50)
    party = models.CharField(max_length=1)
    votesmart_id = models.IntegerField()
    website = models.URLField()
    lis_id = models.CharField(max_length=100)
    leadership_role = models.CharField(max_length=100)
    govtrack_id = models.CharField(max_length=100)
    facebook_id = models.CharField(max_length=100)
    birthday = models.DateField()
    term_start = models.DateField()
    nickname = models.CharField(max_length=100)
    contact_form = models.URLField()
    ocd_id = models.CharField(max_length=100)
    gender= models.CharField(max_length=1)
    name_suffix = models.CharField(max_length=100)
    chamber = models.CharField(max_length=100)
    state_rank = models.CharField(max_length=100)
    fec_ids = models.TextField()