from __future__ import unicode_literals

from django_extensions.db.models import TimeStampedModel

from django.db import models


class Program(TimeStampedModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField()
    runtime = models.IntegerField()
    type = models.CharField(max_length=100)


class Season(TimeStampedModel):
    program = models.ForeignKey('Program')
    number = models.PositiveSmallIntegerField()


class Episode(TimeStampedModel):
    season = models.ForeignKey('Season')
    number = models.PositiveSmallIntegerField()


class Segment(models.Model):
    program = models.ForeignKey('Program')
    episode = models.ForeignKey('Episode', blank=True, null=True)
    duration = models.IntegerField()


# class Type