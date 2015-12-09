from django.contrib import admin

# Register your models here.

from .models import Program
from .models import Segment
from .models import MenuItem
from .models import UserProfile



class MenuItemInline(admin.TabularInline):
    model = MenuItem

class SegmentAdmin(admin.ModelAdmin):
    inlines = [MenuItemInline,]


class SegmentInline(admin.TabularInline):
    model = Segment

class ProgramAdmin(admin.ModelAdmin):
    inlines = [SegmentInline,]


admin.site.register(Program, ProgramAdmin)
admin.site.register(Segment, SegmentAdmin)
admin.site.register(MenuItem)
admin.site.register(UserProfile)
