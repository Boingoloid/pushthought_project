# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User

from congress.models import CongressCounter
from hashtag.models import Hashtag

class Tweet(TimeStampedModel):
    text = models.TextField(max_length=140)
    action = models.OneToOneField('Action')

    def save(self, **kwargs):

        super(Tweet, self).save(**kwargs)


class SaveTweetManager(models.Manager):
    def create(self, text, *args, **kwargs):
        action = super(SaveTweetManager, self).create(**kwargs)
        tweet, saved = Tweet.objects.get_or_create(
            text=text,
            action=action,
        )
        if saved:
            Hashtag.hashtags.parse_mentions(text, action.program)
            return tweet


class Action(TimeStampedModel):
    user = models.ForeignKey(User)
    program = models.ForeignKey('programs.Program', related_name='actions')
    congress = models.ForeignKey('congress.Congress', blank=True, null=True)
    tweets = SaveTweetManager()

    def save(self, **kwargs):
        if not self.id:
            counter, created = CongressCounter.objects.get_or_create(
                program=self.program,
                congress=self.congress,
            )
            counter.increase()
            self.program.increase()
        super(Action, self).save(**kwargs)
