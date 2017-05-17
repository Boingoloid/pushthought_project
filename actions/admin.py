# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from . import models

class TweetInline(admin.StackedInline):
    model = models.Tweet


class ActionAdmin(admin.ModelAdmin):
    model = models.Action
    inlines = (TweetInline, )

admin.site.register(models.Action, ActionAdmin)