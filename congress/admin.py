from django.contrib import admin
from . import models


class CongressInline(admin.StackedInline):
    model = models.Congress

class ZipAdmin(admin.ModelAdmin):
    list_display = ['code', ]
    inlines = [CongressInline]

admin.site.register(models.Zip, ZipAdmin)
admin.site.register(models.Congress)
