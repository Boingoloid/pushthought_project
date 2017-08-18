import requests
import json
import re

from django.views.generic import View
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse

from . import forms, models, serializers


class GetCongressData(View):
    API_URL = "https://congress.api.sunlightfoundation.com/legislators/locate"

    def get(self, request, zip_code, *args, **kwargs):
        self.zip_code = zip_code
        try:
            program_id = re.findall(r'\/program\/(\d+)', self.request.META['HTTP_REFERER'])[0]
        except IndexError:
            program_id = None

        self.request.session['zip'] = zip_code
        queryset = self.get_congress_data_from_db()

        if not queryset:
            queryset = self.get_congress_data_from_api()

        if not queryset:
            return HttpResponseNotFound()

        serializer = serializers.CongressSerializer(queryset, program_id=program_id, many=True)
        # serializer.is_valid()
        return JsonResponse(serializer.data, safe=False)

    def get_congress_data_from_db(self):
        queryset = models.Congress.objects.filter(zips__contains=self.zip_code)
        return queryset

    def get_congress_data_from_api(self):
        req = requests.get(self.get_api_url())
        self.data = json.loads(req.content)['results']
        if self.data:
            congress = self.save_object()
        else:
            congress = None

        return congress

    def get_api_url(self):
        url = '{}?zip={}&apikey={}'.format(self.API_URL, self.zip_code, settings.SUNLIGHT_LABS_API_KEY)

        return url

    def get_existing_congress(self, data):
        bioguide_id = data['bioguide_id']
        try:
            obj = models.Congress.objects.get(bioguide_id=bioguide_id)
        except models.Congress.DoesNotExist:
            obj = None
        return obj


    def save_object(self):
        congress_list = []
        for congress in self.data:
            if self.get_existing_congress(congress):
                obj = self.get_existing_congress(congress)
                obj.add_zip(self.zip_code)
            else:
                congress['zips'] = self.zip_code
                form = forms.CongressForm(congress)
                if form.is_valid():
                    obj = form.save()
                else:
                    obj = None

            if obj:
                congress_list.append(obj.id)

        queryset = models.Congress.objects.filter(id__in=congress_list)
        return queryset


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