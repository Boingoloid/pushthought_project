# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User

from congress.models import CongressCounter


class Tweet(TimeStampedModel):
    text = models.TextField(max_length=140)
    action = models.OneToOneField('Action')


class SaveTweetManager(models.Manager):

    def create(self, text, *args, **kwargs):
        action = super(SaveTweetManager, self).create(**kwargs)
        tweet, saved = Tweet.objects.get_or_create(
            text=text,
            action=action,
        )
        if saved:
            return tweet


class Action(TimeStampedModel):
    user = models.ForeignKey(User)
    program = models.ForeignKey('programs.Program', related_name='counter_model')
    congress = models.ForeignKey('congress.Congress', blank=True, null=True)
    tweets = SaveTweetManager()

    def save(self, **kwargs):
        increase_action = False
        if not self.id:
            increase_action = True
        super(Action, self).save(**kwargs)
        if increase_action:
            counter, created = CongressCounter.objects.get_or_create(
                program=self.program,
                congress=self.congress,
            )
            counter.increase()
            self.program.increase()

