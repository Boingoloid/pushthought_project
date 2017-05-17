from django.contrib import admin
from . import models


class CongressInline(admin.StackedInline):
    model = models.Congress


admin.site.register(models.Congress)
admin.site.register(models.CongressCounter)