from __future__ import unicode_literals

from django_extensions.db.models import TimeStampedModel

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from utils.models import CounterMixin


class Campaign(CounterMixin, TimeStampedModel):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(blank=True, null=True)
    tweet_text = models.TextField(blank=True, null=True)
    email_text = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True, max_length=10000)
    user = models.ForeignKey(User, blank=True, null=True)
    active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('campaign:detail', args=[str(self.slug)])

    def __str__(self):
        return self.slug

    @property
    def email_count(self):
        return self.actions.filter(email__isnull=False).count()

    @property
    def tweet_count(self):
        return self.actions.filter(tweet__isnull=False).count()

    @property
    def action_count(self):
        return self.actions.count()
