from __future__ import unicode_literals
from django_extensions.db.models import TimeStampedModel
from django.db import models
from django.urls import reverse


class Campaign(TimeStampedModel):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    tweet_text = models.TextField(blank=True, null=True)
    email_text = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('campaign:detail', args=[str(self.slug)])