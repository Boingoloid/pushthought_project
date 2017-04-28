import requests
import json
from django.views.generic import DetailView, View
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse

from . import forms
from . import models


class GetCongressData(View):
    API_URL = "https://congress.api.sunlightfoundation.com/legislators/locate"

    def get(self, request, zip_code, *args, **kwargs):
        self.zip_code = zip_code
        self.data = self.get_congress_data_from_api()
        if self.data:
            self.save_object()
            return JsonResponse(self.data, safe=False)
        else:
            return HttpResponseNotFound()

    def get_api_url(self):
        url = self.API_URL + "?zip=" + self.zip_code + "&apikey=" + settings.SUNLIGHT_LABS_API_KEY

        return url

    def get_congress_data_from_api(self):
        req = requests.get(self.get_api_url())
        data = json.loads(req.content)['results']
        return data

    def get_existing_congress(self, data):
        bioguide_id = data['bioguide_id']
        try:
            obj = models.Congress.objects.get(bioguide_id=bioguide_id)
        except models.Congress.DoesNotExist:
            obj = None
        return obj

    def save_or_get_zip(self):
        self.zip, created = models.Zip.objects.get_or_create(code=self.zip_code)
        return self.zip

    def save_object(self):
        self.save_or_get_zip()

        for congress in self.data:
            if self.get_existing_congress(congress):
                obj = self.get_existing_congress(congress)
            else:
                congress['zip'] = self.zip.id
                form = forms.CongressForm(congress)
                if form.is_valid():
                    obj = form.save()

            congress['image'] = obj.image
            congress['full_name'] = obj.full_name

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