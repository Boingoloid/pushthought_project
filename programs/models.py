from __future__ import unicode_literals

from django_extensions.db.models import TimeStampedModel
from django.urls import reverse
from django.db import models


class ProgramManager(models.Manager):
    def documentaries(self):
        return super(ProgramManager, self).get_queryset().filter(type='documentary')

    def webvideos(self):
        return super(ProgramManager, self).get_queryset().filter(type='webvideo')

    def podcasts(self):
        return super(ProgramManager, self).get_queryset().filter(type='podcast')

    def other(self):
        return super(ProgramManager, self).get_queryset().exclude(type='podcast').exclude(type='webvideo').exclude(type='documentary')


class Program(TimeStampedModel):
    title = models.CharField(max_length=100)
    plot_outline = models.TextField()
    image = models.ImageField(blank=True, null=True)
    imdb_id = models.CharField(max_length=10, blank=True, null=True, unique=True)
    runtime = models.IntegerField()
    type = models.CharField(max_length=100)
    objects = ProgramManager()
    users = models.IntegerField(default=0)
    actions = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('programs:detail', args=[str(self.id)])

    def increase(self):
        self.actions += 1
        self.save()
        return True

    def recount_actions(self):
        count = self.action_set.count()
        self.actions = count
        self.save()
        return count


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