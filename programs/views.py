from imdbpie import Imdb
from requests.models import HTTPError

from django.shortcuts import render
from django.views.generic import DetailView, View
from django.http.response import HttpResponse
from django.http import Http404

from utils.helper import url_to_model_field

from . import models, forms

# to be removed:
from pushthought.views import views


class SearchIMDBProgramTitleView(View):
    def get(self, request, *args, **kwargs):
        q = kwargs.get('q', '')
        results = None

        if q:
            imdb = Imdb(anonymize=True)
            results = imdb.search_for_title(q)

        return HttpResponse(results)


class SearchIMDBProgramIDView(View):
    form = forms.ProgramForm

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')

        if not q:
            return HttpResponse('', status=200)

        data = self.get_imdb_data(q)
        existing_program = self.get_program(data.imdb_id)

        if existing_program:
            return HttpResponse('exists', status=200)

        self.save_form(data)

        return HttpResponse('created', status=201)

    def get_imdb_data(self, q):
        imdb = Imdb(anonymize=True)
        try:
            result = imdb.get_title_by_id(q)
        except HTTPError:
            raise Http404
        return result

    def get_program(self, imdb_id):
        try:
            program = models.Program.objects.get(imdb_id=imdb_id)
            return program
        except models.Program.DoesNotExist:
            return None

    def save_form(self, data):
        program_form = self.form(data.__dict__)
        if program_form.is_valid():
            program = program_form.save()
            url_to_model_field(data.poster_url, program.image)


class ProgramDetailView(DetailView):
    model = models.Program
    template_name = 'content_landing_new.html'

    def get_context_data(self, **kwargs):
        context = super(ProgramDetailView, self).get_context_data(**kwargs)

        # context['congressData'] = self.get_congress_data()
        # context['tweetData'] = tweet_data
        # context['hashtagData'] = hashtag_data
        # context['hasCongressData'] = hasCongressData
        return context

    def get_congress_data(self):
        location = self.request.user.extra.location
        current_user = views.get_user_by_token_and_id(self.request)
        try:
            location = current_user['location']
            congress_data = current_user['congressData']
        except:
            try:
                location = self.request.session['location']
                congress_data = self.request.session['congressData']
            except:
                location = None
                congress_data = None

        # if zipcode, load congress people
        try:
            zip = current_user['zip']
        except:
            try:
                zip = self.request.session['zip']
            except:
                zip = None

        # these need
        if location:
            if congress_data:
                hasCongressData = True
                print "loading from location"
                segment_congress_stats = views.get_congress_stats_for_program(segment_id)
                views.add_congress_stats(congress_data, segment_congress_stats)
                if message_list:
                    congress_data = views.add_user_touched_data(congress_data, message_list)
                    # print message_list

        elif zip:
            hasCongressData = True
            congress_data_raw = views.get_congress_data(zip)  # pulls from api or db
            print "loading from zip"
            congress_data_raw = views.add_title_and_full_name(congress_data_raw)
            congress_photos = views.get_congress_photos(congress_data_raw)
            congress_data = views.add_congress_photos(congress_data_raw, congress_photos)
            segment_congress_stats = views.get_congress_stats_for_program(segment_id)
            views.add_congress_stats(congress_data, segment_congress_stats)
            if views.message_list:
                congress_data = views.add_user_touched_data(congress_data, message_list)
                # print message_list
        else:
            hasCongressData = False
            congress_data = []


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


    return render(request, 'content_landing.html',dataDict)