# -*- coding: utf-8 -*-
import re

from django_extensions.db.models import TimeStampedModel
from django.db import models

from utils.models import CounterMixin


class HashtagCounter(CounterMixin, TimeStampedModel):
    program = models.ForeignKey('programs.Program', blank=True, null=True)
    campaign = models.ForeignKey('campaigns.Campaign', blank=True, null=True)
    hashtag = models.ForeignKey('Hashtag')

    class Meta:
        unique_together = ('hashtag', 'program')

    def __unicode__(self):
        s = u"{} ({})".format(self.hashtag, self.counter)
        if self.program:
            s += ' (program "{}")'.format(self.program)
        return s


class HashtagManager(models.Manager):
    def parse_mentions(self, text, program, campaign):
        hashtags = re.findall(r'#(\w+)', text)
        for hashtag_name in hashtags:
            hashtag, created = self.get_or_create(name=hashtag_name)
            counter, created = HashtagCounter.objects.get_or_create(
                hashtag=hashtag, program=program, campaign=campaign)
            counter.increase()


class Hashtag(TimeStampedModel):
    name = models.CharField(max_length=100)
    hashtags = HashtagManager()

    def __unicode__(self):
        return self.name
