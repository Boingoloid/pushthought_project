from __future__ import unicode_literals

from django_extensions.db.models import TimeStampedModel

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Campaign(TimeStampedModel):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    tweet_text = models.TextField(blank=True, null=True)
    email_text = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    active = models.BooleanField(default=True, blank=True)

    def get_absolute_url(self):
        return reverse('campaign:detail', args=[str(self.slug)])

    def __str__(self):
        return self.slug