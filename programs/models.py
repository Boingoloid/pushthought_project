from __future__ import unicode_literals
import math

from django_extensions.db.models import TimeStampedModel
from django.urls import reverse
from django.db import models

from utils.models import CounterMixin


class ProgramManager(models.Manager):
    def documentaries(self):
        return super(ProgramManager, self).get_queryset().filter(type='documentary')

    def webvideos(self):
        return super(ProgramManager, self).get_queryset().filter(type='webvideo')

    def podcasts(self):
        return super(ProgramManager, self).get_queryset().filter(type='podcast')

    def other(self):
        return super(ProgramManager, self).get_queryset().exclude(type='podcast').exclude(type='webvideo').exclude(type='documentary')


class Program(CounterMixin, TimeStampedModel):
    title = models.CharField(max_length=200)
    plot_outline = models.TextField(blank=True)
    image = models.ImageField(blank=True, null=True)
    imdb_id = models.CharField(max_length=10, blank=True, null=True)
    runtime = models.IntegerField()
    type = models.CharField(max_length=100)
    youtube_id = models.CharField(max_length=15, blank=True, null=True)
    users = models.IntegerField(default=0)

    objects = ProgramManager()

    def __unicode__(self):
        if self.imdb_id:
            source = u"IMDB {}".format(self.imdb_id)
        elif self.youtube_id:
            source = u"Youtube {}".format(self.youtube_id)
        else:
            source = u"(no source)"
        return u"{} ({}) {}".format(self.title, self.type, source)

    @property
    def url(self):
        if self.imdb_id:
            return 'http://www.imdb.com/title/{}/'.format(self.imdb_id)
        elif self.youtube_id:
            return 'https://www.youtube.com/watch?v={}'.format(self.youtube_id)

    @property
    def runtime_minutes(self):
        return self.runtime / 60

    def congres_counter(self, bioguide_id):
        counter = self.congresscounter_set.get(congress__bioguide_id=bioguide_id).counter
        return counter

    def get_absolute_url(self):
        return reverse('programs:detail', args=[str(self.id)])

#
#
# class Season(TimeStampedModel):
#     program = models.ForeignKey('Program')
#     number = models.PositiveSmallIntegerField()
#
#     def __str__(self):
#         return '{} season {}'.format(self.program, self.number)
#
#
# class Episode(TimeStampedModel):
#     season = models.ForeignKey('Season')
#     number = models.PositiveSmallIntegerField()
#
#     def __str__(self):
#         return ' {} episode {}'.format(self.season, self.number)
#
#
# class Segment(TimeStampedModel):
#     program = models.ForeignKey('Program', blank=True, null=True)
#     episode = models.ForeignKey('Episode', blank=True, null=True)
#     duration = models.IntegerField()
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     url = models.URLField(blank=True, null=True)
#
#     def __str__(self):
#         return '{}'.format(self.program)
