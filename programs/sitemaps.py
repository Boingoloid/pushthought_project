from django.contrib.sitemaps import Sitemap
from .models import Program


class ProgramSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Program.objects.all()

    def lastmod(self, obj):
        return obj.modified