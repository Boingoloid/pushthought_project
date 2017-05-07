import requests
import json
from django.views.generic import View
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse

from . import forms, models, serializers


class GetCongressData(View):
    API_URL = "https://congress.api.sunlightfoundation.com/legislators/locate"

    def get(self, request, zip_code, *args, **kwargs):
        self.zip_code = zip_code
        self.zip_obj = self.get_zip_object()

        if not self.zip_obj:
            return HttpResponseNotFound()

        serializer = serializers.CongressSerializer(self.zip_obj.congress_set, many=True)
        return JsonResponse(serializer.data, safe=False)


    def get_zip_object(self):
        zip_obj = models.Zip.objects.filter(code=self.zip_code).first()

        if zip_obj:
            return zip_obj

        self.data = self.get_congress_data_from_api()
        if self.data:
            zip_obj = self.save_object()

        return zip_obj

    def get_api_url(self):
        url = '{}?zip={}&apikey={}'.format(self.API_URL, self.zip_code, settings.SUNLIGHT_LABS_API_KEY)

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
        zip, created = models.Zip.objects.get_or_create(code=self.zip_code)
        return zip

    def save_object(self):
        self.zip = self.save_or_get_zip()

        for congress in self.data:
            if self.get_existing_congress(congress):
                obj = self.get_existing_congress(congress)
            else:
                congress['zip'] = self.zip.id
                form = forms.CongressForm(congress)
                if form.is_valid():
                    obj = form.save()


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