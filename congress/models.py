from __future__ import unicode_literals

from django_extensions.db.models import TimeStampedModel

from django.db import models
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.validators import validate_comma_separated_integer_list

from utils.models import CounterMixin

class Congress(TimeStampedModel):
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    state_name = models.CharField(max_length=30)
    state = models.CharField(max_length=5)
    oc_email = models.EmailField(blank=True, null=True)
    title = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)
    twitter_id = models.CharField(max_length=30, blank=True, null=True)
    bioguide_id = models.CharField(max_length=30, unique=True)
    office = models.CharField(max_length=100, blank=True, null=True)
    thomas_id = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    senate_class = models.IntegerField(blank=True, null=True)
    term_end = models.DateField(blank=True, null=True)
    crp_id = models.CharField(max_length=50, blank=True, null=True)
    party = models.CharField(max_length=1, blank=True, null=True)
    votesmart_id = models.IntegerField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    lis_id = models.CharField(max_length=100, blank=True, null=True)
    leadership_role = models.CharField(max_length=100, blank=True, null=True)
    govtrack_id = models.CharField(max_length=100, blank=True, null=True)
    facebook_id = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    term_start = models.DateField(blank=True, null=True)
    nickname = models.CharField(max_length=100, blank=True, null=True)
    contact_form = models.URLField(blank=True, null=True)
    ocd_id = models.CharField(max_length=100, blank=True, null=True)
    gender= models.CharField(max_length=1, blank=True, null=True)
    name_suffix = models.CharField(max_length=100, blank=True, null=True)
    chamber = models.CharField(max_length=100, blank=True, null=True)
    state_rank = models.CharField(max_length=100, blank=True, null=True)
    fec_ids = models.TextField(blank=True, null=True)
    zips = models.CharField(max_length=1000, validators=[validate_comma_separated_integer_list], blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def full_name(self):
        if self.middle_name:
            name = '{} {} {}'.format(self.first_name, self.middle_name, self.last_name)
        else:
            name = '{} {}'.format(self.first_name, self.last_name)
        return name

    @property
    def image(self):
        file_name = '{}.jpg'.format(self.bioguide_id.upper())
        url = static('img/congress/{}'.format(file_name))
        return url

    def add_zip(self, zip_code):
        if not self.zips:
            self.zips = zip_code
            self.save()
            return True

        if zip_code not in self.zips:
            self.zips += ',{}'.format(zip_code)
            self.save()
            return True

    def remove_zip(self, zip):
        self.zips = self.zips.replace(',{}'.format(zip), '')
        self.save()
        return self.zips


class CongressCounter(CounterMixin, TimeStampedModel):
    program = models.ForeignKey('programs.Program')
    congress = models.ForeignKey('Congress')

    class Meta:
        unique_together = ('congress', 'program')

    # def recount(self):
    #     count = Action.objects.filter(receiver=self.congress, program=self.program)
    #     return count