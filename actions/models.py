# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User


class Tweet(TimeStampedModel):
    text = models.TextField(max_length=140)
    action = models.OneToOneField('Action')


class SaveTweetManager(models.Manager):

    def create(self, text, *args, **kwargs):
        action = super(SaveTweetManager, self).create(**kwargs)
        tweet, saved = Tweet.objects.get_or_create(text=text, action=action)
        if saved:
            return tweet

    def get(self, *args, **kwargs):
        return super(SaveTweetManager, self).get(*args, **kwargs)


class Action(TimeStampedModel):
    user = models.ForeignKey(User)
    program = models.ForeignKey('programs.Program')
    tweets = SaveTweetManager()

    def save(self, **kwargs):
        increase_action = False
        if not self.id:
            increase_action = True
        super(Action, self).save(**kwargs)
        if increase_action:
            self.program.increase()

