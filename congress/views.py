import requests
import json
import re

from django.views.generic import View
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse

from . import forms, models, serializers


class GetCongressData(View):
    serializer = serializers.CongressSerializer
    regex = r'\/program\/(\d+)'

    def get(self, request, zip_code, *args, **kwargs):
        self.zip_code = zip_code
        request.session['zip'] = zip_code
        if self.request.user.is_authenticated():
            if self.request.user.profile.zip != zip_code:
                self.request.user.profile.zip = zip_code
                self.request.user.profile.save(update_fields=['zip'])
        try:
            program_id = re.findall(self.regex, self.request.META['HTTP_REFERER'])[0]
        except IndexError, KeyError:
            program_id = None

        queryset = self.get_congress_data_from_db()

        if not queryset:
            return HttpResponseNotFound()

        serializer = self.serializer(queryset, program_id=program_id, many=True)
        return JsonResponse(serializer.data, safe=False)

    def get_congress_data_from_db(self):
        queryset = models.Congress.objects.filter(zips__contains=self.zip_code)
        return queryset


class GetCongressCampaignData(GetCongressData):
    serializer = serializers.CongressCampaignSerializer
    regex = r'\/c\/(\w+)'


class GetCongressDataLocation(GetCongressData):

    def get(self, request, *args, **kwargs):
        self.lat = request.GET.get('lat')
        self.long = request.GET.get('long')
        self.data = self.get_congress_data_from_api()
        if self.data:
            self.save_object()
            return HttpResponse('Created')
        else:
            return HttpResponseNotFound()

    def get_api_url(self):
        url = self.API_URL + "?latitude=" + str(self.lat) + "&longitude=" + str(self.long) + "&apikey=" + settings.SUNLIGHT_LABS_API_KEY

        return url
