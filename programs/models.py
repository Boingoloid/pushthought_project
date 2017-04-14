from __future__ import unicode_literals

from django_extensions.db.models import TimeStampedModel

from django.db import models


class Program(TimeStampedModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(blank=True, null=True)
    runtime = models.IntegerField()
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Season(TimeStampedModel):
    program = models.ForeignKey('Program')
    number = models.PositiveSmallIntegerField()

    def __str__(self):
        return '{} season {}'.format(self.program, self.number)


class Episode(TimeStampedModel):
    season = models.ForeignKey('Season')
    number = models.PositiveSmallIntegerField()

    def __str__(self):
        return ' {} episode {}'.format(self.season, self.number)


class Segment(models.Model):
    program = models.ForeignKey('Program')
    episode = models.ForeignKey('Episode', blank=True, null=True)
    duration = models.IntegerField()

    def __str__(self):
        return '{}'.format(self.program)