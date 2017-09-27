import requests
import json
import re
from imdbpie import Imdb

from django.shortcuts import render
from django.views.generic import DetailView, View
from django.http.response import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.contrib import messages

from utils.helper import url_to_model_field
from youtube.quickstart import videos_list_by_id

from . import models, forms


class SearchIMDBProgramTitleView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
        results = None

        if q:
            imdb = Imdb(anonymize=True)
            results = imdb.search_for_title(q)[:5]

        return HttpResponse(results)


class ParseProgramIDView(View):
    form = forms.ProgramForm

    def get(self, request, *args, **kwargs):
        imdb_id = self.parse_imdb_id()
        youtube_id = self.parse_youtube_id()

        if not imdb_id and not youtube_id:
            return self.get_redirect_to_ref()

        if imdb_id:
            data = self.get_imdb_data(imdb_id)
            if data:
                program_filter = dict(imdb_id=data.imdb_id)
        else:
            data = self.get_youtube_data(youtube_id)
            program_filter = dict(youtube_id=youtube_id)

            if data['items']:
                snippet = data['items'][0]['snippet']
                title = '{} ({})'.format(snippet['title'], snippet['channelTitle'])
                runtime = self.parse_runtime(data['items'][0]['contentDetails']['duration'])

                try:
                    poster_url = snippet['thumbnails']['standard']['url']
                except KeyError:
                    poster_url = ''

                data = {
                    'title': title,
                    'plot_outline': '', #snippet['description'],
                    'runtime': runtime,
                    'poster_url': poster_url,
                    'type': 'webvideo',
                    'youtube_id': youtube_id,
                }
            else:
                data = ''

        if not data:
            return self.get_redirect_to_ref()

        program = self.get_program(program_filter)

        if not program:
            program = self.save_form(data)

        return HttpResponseRedirect(program.get_absolute_url())

    def parse_imdb_id(self):
        q = self.request.GET.get('q', '')
        pattern = 'imdb\.com\/title\/(\w+)'
        id = re.findall(pattern, q)
        if len(id) == 0:
            return False
        return id[0]

    def parse_youtube_id(self):
        q = self.request.GET.get('q', '')
        pattern = 'youtube\.com\/watch\?v=(.{11})'
        id = re.findall(pattern, q)
        if len(id) == 0:
            return False
        return id[0]

    @staticmethod
    def parse_runtime(duration):
        pattern = '^PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$'
        match = re.findall(pattern, duration)[0]
        minutes = match[1]
        hours = match[0]
        runtime = 0

        if minutes:
            runtime = int(minutes)

        if hours:
            runtime += 60 * int(hours)

        return runtime

    def get_imdb_data(self, id):
        imdb = Imdb(anonymize=True)
        try:
            result = imdb.get_title_by_id(id)
        except requests.HTTPError:
            result = None

        return result

    def get_youtube_data(self, id):
        try:
            result = videos_list_by_id(id)
        except:
            result = None

        return result

    def get_program(self, filter):
        try:
            program = models.Program.objects.get(**filter)
            return program
        except models.Program.DoesNotExist:
            return None

    def save_form(self, data):
        try:
            data = data.__dict__
            poster_url = data.poster_url
        except AttributeError:
            poster_url = data['poster_url']

        program_form = self.form(data)
        if program_form.is_valid():
            program = program_form.save()
            url_to_model_field(poster_url, program.image)
            messages.add_message(self.request, messages.INFO,
                                 'Congrats, you are the first person to create this page on Push Thought.')
            return program

    def get_redirect_to_ref(self):
        url = self.request.META.get('HTTP_REFERER')
        messages.add_message(self.request, messages.WARNING, 'Your program not found!')
        return HttpResponseRedirect(url)


class SearchYoutubeProgramTitleView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
        results = None

        # if q:
        #     a = youtube_search(q, 25)

        return HttpResponse(results)


class ProgramDetailView(DetailView):
    model = models.Program
    template_name = 'content_landing.html'

    def get_context_data(self, **kwargs):
        context = super(ProgramDetailView, self).get_context_data(**kwargs)

        if self.request.session.get('alertList'):
            context['alertList'] = self.request.session['alertList']
            del self.request.session['alertList']
        return context
    #
    # def get_congress_data(self):
    #     location = self.request.user.extra.location
    #     current_user = views.get_user_by_token_and_id(self.request)
    #     try:
    #         location = current_user['location']
    #         congress_data = current_user['congressData']
    #     except:
    #         try:
    #             location = self.request.session['location']
    #             congress_data = self.request.session['congressData']
    #         except:
    #             location = None
    #             congress_data = None
    #
    #     # if zipcode, load congress people
    #     try:
    #         zip = current_user['zip']
    #     except:
    #         try:
    #             zip = self.request.session['zip']
    #         except:
    #             zip = None
    #
    #     # these need
    #     if location:
    #         if congress_data:
    #             hasCongressData = True
    #             print "loading from location"
    #             segment_congress_stats = views.get_congress_stats_for_program(segment_id)
    #             views.add_congress_stats(congress_data, segment_congress_stats)
    #             if message_list:
    #                 congress_data = views.add_user_touched_data(congress_data, message_list)
    #                 # print message_list
    #
    #     elif zip:
    #         hasCongressData = True
    #         congress_data_raw = views.get_congress_data(zip)  # pulls from api or db
    #         print "loading from zip"
    #         congress_data_raw = views.add_title_and_full_name(congress_data_raw)
    #         congress_photos = views.get_congress_photos(congress_data_raw)
    #         congress_data = views.add_congress_photos(congress_data_raw, congress_photos)
    #         segment_congress_stats = views.get_congress_stats_for_program(segment_id)
    #         views.add_congress_stats(congress_data, segment_congress_stats)
    #         if views.message_list:
    #             congress_data = views.add_user_touched_data(congress_data, message_list)
    #             # print message_list
    #     else:
    #         hasCongressData = False
    #         congress_data = []


def content_landing(request, segment_id):
    # get program and segment ID
    # store ID's in session
    program_id = segment_id
    try:
        request.session['programId'] = program_id
        request.session['segmentId'] = segment_id
    except:
        print "error in top of content landing saving request.session segment and program ids - passing on."

    program_result = fetch_program_data(segment_id)
    tweet_data = get_tweet_data(segment_id)
    hashtag_data = get_hashtag_data(segment_id)

    # get user and sentMessage list
    current_user = get_user_by_token_and_id(request)
    if current_user:
        request.session['currentUser'] = current_user
        message_list = get_segment_actions_for_user(segment_id,current_user['objectId'])
        #get email fields

    else:
        message_list = []


    # if location, load congress people (try user, then session)
    try:
        location = current_user['location']
        congress_data = current_user['congressData']
    except:
        try:
            location = request.session['location']
            congress_data = request.session['congressData']
        except:
            location = None
            congress_data = None

    # if zipcode, load congress people
    try:
        zip = current_user['zip']
    except:
        try:
            zip = request.session['zip']
        except:
            zip = None

    # these need
    if location:
        if congress_data:
            hasCongressData = True
            print "loading from location"
            segment_congress_stats = get_congress_stats_for_program(segment_id)
            add_congress_stats(congress_data, segment_congress_stats)
            if message_list:
                congress_data = add_user_touched_data(congress_data, message_list)
                # print message_list

    elif zip:
        hasCongressData = True
        congress_data_raw = get_congress_data(zip) #pulls from api or db
        print "loading from zip"
        congress_data_raw = add_title_and_full_name(congress_data_raw)
        congress_photos = get_congress_photos(congress_data_raw)
        congress_data = add_congress_photos(congress_data_raw, congress_photos)
        segment_congress_stats = get_congress_stats_for_program(segment_id)
        add_congress_stats(congress_data, segment_congress_stats)
        if message_list:
            congress_data = add_user_touched_data(congress_data, message_list)
            # print message_list
    else:
        hasCongressData = False
        congress_data = []


    # create dataDict to send with response.
    dataDict = {}
    # inclue alert list, if returning from an action, these alerts will display on load
    try:
        dataDict['alertList'] = request.session['alertList']
        del request.session['alertList']
        request.session.modified = True
    except:
        print "no alertList to display"

    dataDict['programId'] = program_id
    dataDict['segmentId'] = segment_id
    dataDict['program'] = program_result
    dataDict['currentUser'] = current_user
    dataDict['congressData'] = congress_data
    dataDict['tweetData'] = tweet_data
    dataDict['hashtagData'] = hashtag_data
    dataDict['hasCongressData'] = hasCongressData


    return render(request, 'content_landing_old.html', dataDict)


class GetCongressByZip(View):
    API = "https://congress.api.sunlightfoundation.com/legislators/locate"

    def get(self, request, zip, *args, **kwargs):
        self.zip = zip
        self.save_zip()
        json_data = self.get_congress_data()
        json_data = self.add_title_and_full_name(json_data)

    def save_zip(self):
        self.request.user.extra.zip = self.zip
        self.request.user.save()

    def get_congress_data(self):
        urlAPI = self.API + "?zip=" + self.zip + "&apikey=" + settings.SUNLIGHT_LABS_API_KEY
        r = requests.get(urlAPI)
        results = json.loads(r.content)['results']
        return results

    def add_title_and_full_name(self, json_data):
        for item in json_data:
            # Create full_name
            item['full_name'] = item['first_name'] + " " + item['last_name']
            # Create Title
            if item['title'] == "Rep":
                item['title'] = "Rep, " + item['state'] + " - d:" + str(item['district'])
            else:
                item['title'] = "Senator, " + item['state']
        return json_data



def get_congress_with_zip(request, zip):
    # Return congress based on zip
    congress_data_raw = get_congress_data(zip)
    congress_data_raw = add_title_and_full_name(congress_data_raw)
    congress_photos = get_congress_photos(congress_data_raw)
    congress_data = add_congress_photos(congress_data_raw,congress_photos)
    congress_data = add_congress_stats(congress_data,segment_congress_stats)

    if message_list:
        congress_data = add_user_touched_data(congress_data, message_list)
    print "made it here, sending success response with congressData"
    return congress_data

def get_congress_data(zip_code):
    root = "https://congress.api.sunlightfoundation.com/legislators/locate"

    #HELPER FUNCTION: nested function to get Congress Data from api, then save in CongressData under the zip_code
    def get_congress_data_from_api():
        urlAPI = root + "?zip=" + zip_code + "&apikey=" + settings.SUNLIGHT_LABS_API_KEY
        r = requests.get(urlAPI)
        results = json.loads(r.content)['results']
        if len(results) != 0:
            save_result = save_to_congress_data_collection()
        return results

    #MAIN: Checks UPDATE TRIGGER, then uses method above to get data locally or form api
    if not settings.CONGRESS_DATA_UPDATE_TRIGGER:
        congress_data = db.CongressData.find_one({"zip_code":zip_code})
        if congress_data:
            # print "congress data returned local, no api used", congress_data
            return congress_data['results']
        else:
            print "no congress for that zip"
            return get_congress_data_from_api()
    else:
        results = get_congress_data_from_api()

        # if results, delete existing zip data and add new
        if len(results) != 0:
            delete_result = db.CongressData.delete_many({"zip_code": zip_code})
            print "deleted CongressData documents count:", delete_result.deleted_count
            save_result = save_to_congress_data_collection(zip_code, results)
            print "saved CongressData document:", save_result
            return results
        else:
            return results