# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django_extensions.db.models import TimeStampedModel

from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from allauth.socialaccount.models import SocialAccount


class Profile(TimeStampedModel):
    user = models.OneToOneField(User)
    location = models.CharField(max_length=100, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)

    @property
    def twitter(self):
        token = SocialAccount.objects.filter(user=self.user, provider='twitter').first()
        if token:
            return token.extra_data['screen_name']

    def __str__(self):
        return '{}'.format(self.user)


@receiver(post_save, sender=User)
def create_extra_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class SubscriberEmail(TimeStampedModel):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email