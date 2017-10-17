# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User

from congress.models import CongressCounter
from hashtag.models import Hashtag
from users.models import Profile

class Tweet(TimeStampedModel):
    text = models.TextField(blank=True)
    action = models.OneToOneField('Action')


class Email(TimeStampedModel):
    text = models.TextField(blank=True)
    action = models.OneToOneField('Action')
    fields = models.TextField(null=True, blank=True)
    is_sent = models.NullBooleanField()


class SaveTweetManager(models.Manager):
    def create(self, text, *args, **kwargs):
        action = super(SaveTweetManager, self).create(**kwargs)
        tweet, created = Tweet.objects.get_or_create(
            text=text,
            action=action,
        )
        if created:
            Hashtag.hashtags.parse_mentions(text, action.program)
            return tweet


class SaveEmailManager(models.Manager):
    def create(self, text, fields, is_sent, *args, **kwargs):
        if 'user' not in kwargs:
            kwargs['user'] = User.objects.update_or_create(
                email=fields['$EMAIL'],
                defaults={'first_name': fields['$NAME_FIRST'],
                          'last_name': fields['$NAME_LAST'],
                          'username': fields['$EMAIL']})[0]
        Profile.objects.update_or_create(
            user=kwargs['user'],
            defaults=dict(
                prefix=fields.get('$NAME_PREFIX'),
                street=fields.get('$ADDRESS_STREET'),
                city=fields.get('$ADDRESS_CITY'),
                phone=fields.get('$PHONE'),
                zip=fields.get('$ADDRESS_ZIP5')))
        action = super(SaveEmailManager, self).create(**kwargs)
        return Email.objects.create(text=text, action=action, fields=fields,
                                    is_sent=is_sent)


class Action(TimeStampedModel):
    user = models.ForeignKey(User, blank=True, null=True)
    program = models.ForeignKey('programs.Program', related_name='actions', blank=True, null=True)
    campaign = models.ForeignKey('campaigns.Campaign', related_name='actions', blank=True, null=True)
    congress = models.ForeignKey('congress.Congress')
    tweets = SaveTweetManager()
    emails = SaveEmailManager()

    def save(self, **kwargs):
        if not self.id:

            values = dict(
                congress=self.congress,
                program=None,
                campaign=None
            )

            if self.program:
                values['program'] = self.program
            if self.campaign:
                values['campaign'] = self.campaign

            counter, created = CongressCounter.objects.get_or_create(**values)
            counter.increase()
            if self.program:
                self.program.increase()

            if self.campaign:
                self.campaign.increase()

        super(Action, self).save(**kwargs)
