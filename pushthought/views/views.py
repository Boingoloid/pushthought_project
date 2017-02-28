from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.conf import settings
from django.template import RequestContext
from django.contrib import messages

from corsheaders.defaults import default_methods

# from django.contrib.auth import authenticate, login
# from pushthought.forms import UserForm, UserProfileForm
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User

from django.contrib.sessions.models import Session


from ..models import Segment
from ..models import MenuItem

# views import

from views_twtitter_auth import *
from views_parse_user import *
from views_api import *
from views_get_data import *
from views_alerts import *
from views_user_forms import *
from views_congress import *

# from django.contrib.auth import logout

import tweepy
import json, httplib
import pymongo

PARSE_APP_ID = 'lzb0o0wZHxbgyIHSyZLlooijAK9afoyN8RV4XwcM'
PARSE_REST_KEY = 'YTeYDL8DeSDNsmZT219Lp8iXgPZ24ZGu3ywUjo23'
TWITTER_CALLBACK_ROOT_URL = settings.TWITTER_CALLBACK_ROOT_URL
# TWITTER_CALLBACK_ROOT_URL = 'http://www.pushthought.com/verify_catch'

TWITTER_CONSUMER_KEY = settings.TWITTER_CONSUMER_KEY
TWITTER_CONSUMER_SECRET = settings.TWITTER_CONSUMER_SECRET

MONGODB_URI = settings.MONGODB_URI
# Create your views here.

def home(request):
    program_list = get_program_list()
    dataDict = {}
    dataDict['programList'] = program_list
    # print program_list
    return render(request, 'home.html', dataDict)

def submit_email(request,email):
    # print email
    emailString = email.decode()
    connection2 = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connection2.connect()
    connection2.request('POST', '/parse/classes/EmailsSubmitted', json.dumps({
        "email": emailString
        }), {
        "X-Parse-Application-Id": PARSE_APP_ID,
        "X-Parse-REST-API-Key": PARSE_REST_KEY,
        "Content-Type": "application/json"
    })
    result = json.loads(connection2.getresponse().read())
    return HttpResponseRedirect('/home/')

def contact(request):
    context_instance=RequestContext(request)
    return render(request, 'contact.html')

def send_contact(request):
    print "send contact function!"
    print request.body
    print request.GET
    print request.POST
    print request.session
    print request.META
    context_instance=RequestContext(request)
    contact_data = json.loads(request.body)
    print contact_data

    client = pymongo.MongoClient(MONGODB_URI)
    db = client.get_default_database()
    saveReturn = db.contact_form.save(contact_data)
    print saveReturn

    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def leaving(request):
    return HttpResponse("Watch function not in place yet, working on it. thanks :)")


def browse(request):
    program_list = get_program_list()
    program_stats = get_program_browse_stats()
    # program_list_with_stats = get_program_list_with_stats(program_list,program_stats)
    stats_list = get_program_browse_stats_user_count()
    program_list_with_stats = combine_programs_with_stats(program_list,stats_list)

    documentaryArray = []
    webVideoArray = []
    podcastArray = []
    otherArray = []

    # sort and divide
    for item in program_list_with_stats:
        category = item['tagCustom']
        if category == 'documentary':
            documentaryArray.append(item)
        elif category == 'webvideo':
            webVideoArray.append(item)
        elif category == 'podcast':
            podcastArray.append(item)
        else:
            otherArray.append(item)

    print "doc Video", len(documentaryArray)
    print "web Video", len(webVideoArray)
    print "podcast", len(podcastArray)
    print "other", len(otherArray)

    dataDict = {}
    dataDict['programList'] = program_list_with_stats
    dataDict['segmentList'] = segment_list
    dataDict['documentaryList'] = documentaryArray
    dataDict['webVideoList'] = webVideoArray
    dataDict['podcastList'] = podcastArray
    dataDict['otherList'] = otherArray

    return render(request, 'browse.html', dataDict)

def get_user_by_token_and_id(request):
    try:
        sessionToken = request.session['sessionToken']
        userObjectId = request.session['userObjectId']
    except:
        sessionToken = None
        userObjectId = None

    if sessionToken and userObjectId:
        connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
        connection.connect()
        connection.request('GET', '/parse/classes/_User/' + userObjectId, '', {
                "X-Parse-Application-Id": PARSE_APP_ID,
                "X-Parse-REST-API-Key": PARSE_REST_KEY,
                "X-Parse-Session-Token": sessionToken
             })
        current_user = json.loads(connection.getresponse().read())
        return current_user
    else:
        return None

def get_segment_actions_for_user(segmentId,userObjectId):
    # GET current value for segment activity
    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    params = urllib.urlencode({
        "where":json.dumps({
            "segmentObjectId": segmentId,
            "userObjectId": userObjectId
        })
    })
    connection.connect()
    connection.request('GET', '/parse/classes/SentMessages?%s' % params, '', {
       "X-Parse-Application-Id": PARSE_APP_ID,
       "X-Parse-REST-API-Key": PARSE_REST_KEY
     })
    result = json.loads(connection.getresponse().read())
    messaage_list = result['results']
    return messaage_list

def content_landing(request, programId):
    # get program and segment ID
    # store ID's in session
    segmentId = programId
    request.session['programId'] = programId
    request.session['segmentId'] = segmentId



    # get program object and Tweet/# activity for the program's landing page
    program_result = fetch_program_data(programId)
    tweet_data = get_tweet_data(programId)
    hashtag_data = get_hashtag_data(segmentId)

    # get user and sentMessage list
    current_user = get_user_by_token_and_id(request)
    request.session['currentUser'] = current_user

    if current_user:
        message_list = get_segment_actions_for_user(segmentId,current_user['objectId'])
    else:
        message_list = []

    # if zipcode, load congress people
    try:
        zip = current_user['zip']
    except:
        zip = None

    if zip:
        hasCongressData = True
        congress_data_raw = get_congress_data(zip)
        congress_data_raw = add_title_and_full_name(congress_data_raw)
        congress_photos = get_congress_photos(congress_data_raw)
        congress_data = add_congress_photos(congress_data_raw, congress_photos)
        # congress_data = add_prior_activity_to_congress_data(congress_data, message_list)
    else:
        hasCongressData = False
        congress_data = [
            {
                "full_name": "Congressperson",
                "title": "state / district"
            },
            {
                "full_name": "Congressperson",
                "title": "state / district"
            },
            {
                "full_name": "Congressperson",
                "title": "state / district"
            }
        ]

    # create dataDict to send with response.
    dataDict = {}
    # inclue alert list, if returning from an action, these alerts will display on load
    try:
        dataDict['alertList'] = request.session['alertList']
        del request.session['alerList']
    except:
        print "no alertList to display"

    dataDict['program'] = program_result
    dataDict['programId'] = programId
    dataDict['segmentId'] = segmentId
    dataDict['currentUser'] = current_user
    dataDict['congressData'] = congress_data
    dataDict['tweetData'] = tweet_data
    dataDict['hashtagData'] = hashtag_data
    dataDict['hasCongressData'] = hasCongressData

    return render(request, 'content_landing.html',dataDict)

def content_landing_empty(request):
    try:
        programId = request.session['programId']
        # del request.session['programId']
        print "Content_landing_empty, passing on programId:", programId
        dataDict = {}
        dataDict['programId'] = programId
        return render(request, 'content_landing_empty.html',dataDict)
    except:
        return HttpResponseRedirect('/browse/')



def get_congress(request,zip):
    # Save zip to Session
    request.session['zip'] = zip

    # Save zip to user: try
    save_result = save_zip_to_user(request, zip)
    print "zip to user result:", save_result

    # Return congress based on location
    congress_data_raw = get_congress_data(zip)
    congress_data_raw = add_title_and_full_name(congress_data_raw)
    congress_photos = get_congress_photos(congress_data_raw)
    congress_data = add_congress_photos(congress_data_raw,congress_photos)
    return HttpResponse(json.dumps({'congressData': congress_data}), content_type="application/json")

def save_zip_to_user(request,zip):
    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connection.connect()
    connection.request('PUT', '/parse/classes/_User/' + request.session['currentUser']['objectId'], json.dumps({
            "zip": zip,
        }),
        {
            "X-Parse-Application-Id": PARSE_APP_ID,
            "X-Parse-REST-API-Key": PARSE_REST_KEY,
            "X-Parse-Session-Token": request.session['sessionToken'],
            "Content-Type": "application/json"
        })
    result = json.loads(connection.getresponse().read())
    return result


def fed_rep_action_menu(request, programId, segmentId):

    # Get variables
    program_dict = fetch_program_data(programId)
    segment_dict = fetch_segment_data(segmentId)
    program_data = json.dumps(program_dict)
    segment_data = json.dumps(segment_dict)
    action_list = fetch_action_list(segmentId)

    zipCode = "94107"
    congress_data_raw = get_congress_data(zipCode)
    congress_data_raw = add_title_and_full_name(congress_data_raw)
    congress_photos = get_congress_photos(congress_data_raw)
    congress_data = add_congress_photos(congress_data_raw,congress_photos)

    hashtag_data = get_hashtag_data(segmentId)

    tweet_data = get_tweet_data(segmentId)

    # Store values in session
    source_url = request.build_absolute_uri()
    request.session['last_menu_url'] = source_url
    print "source_url saved in session:" + source_url
    request.session['programId'] = programId
    request.session['segmentId'] = segmentId

    dataDict = {}
    dataDict['actionList'] = action_list
    dataDict['hashtagData'] = hashtag_data
    dataDict['tweetData'] = tweet_data
    dataDict['congressData'] = congress_data

    dataDict['programId'] = programId
    dataDict['programTitle'] = program_dict['programTitle']
    dataDict['programData'] = program_data

    dataDict['segmentId'] = segmentId
    dataDict['segmentTitle'] = segment_dict['segmentTitle']
    dataDict['purposeSummary'] = segment_dict['purposeSummary']
    dataDict['segmentData'] = segment_data

    return render(request, 'fed_rep_action_menu.html', dataDict)


def program_detail(request,programId):

    # if documentary
    client = pymongo.MongoClient(MONGODB_URI)
    db = client.get_default_database()
    program = db.Programs.find_one({"_id":programId})
    # program_dict = fetch_program_data(programId)
    # segment_list = get_segment_list(programId)

    print "print program"
    print program

    dataDict = {}
    dataDict['program'] = program
    # dataDict['programDict'] = program_dict
    # dataDict['segmentList'] = segment_list
    # dataDict['programObjectId'] = program_dict['objectId']

    return render(request, 'program_detail.html',dataDict)

# Use the login_required() decorator to ensure only those logged in can access the view.
# @login_required

from django.core.urlresolvers import reverse
from django.shortcuts import redirect

def account_home(request, user_pk):


    dataDict = {}
    try:
        session_token = request.session['sessionToken']
        print "session token top of account home:" + session_token
        current_user = get_user_in_parse_only(request, user_pk)
        dataDict['current_user'] = current_user

        programs = get_program_list_for_user(user_pk)
        dataDict['programs'] = programs
        print programs

    except:
        print "no session token available on account home"
        print "no current user so redirecting to Sign In"
        return redirect(reverse('user_signin_form'))

    dataDict['user_pk'] = user_pk

    #programs = Program.objects.filter(user=user_pk)
    # dataDict['programs'] = programs

    return render(request, 'account_home.html', dataDict)




# @login_required
def segment_list(request, user_pk, program_pk):
    program = get_object_or_404(Program, pk=program_pk)
    segments = Segment.objects.filter(program__pk=program_pk)

    # Entry.objects.filter(blog__name='Beatles Blog')
    #   get_list_or_404(Segment, program= program_pk)

    dataDict = {}
    dataDict['user_pk'] = user_pk
    dataDict['segments'] = segments
    dataDict['program'] = program
    return render(request, 'segment_list.html', dataDict)


# @login_required
def segment_menu(request, user_pk, program_pk, segment_pk):
    menuItems = MenuItem.objects.filter(segment__pk=segment_pk)
    segment = get_object_or_404(Segment, pk=segment_pk)
    program = get_object_or_404(Program, pk=program_pk)

    dataDict = {}
    dataDict['menuItems'] = menuItems
    dataDict['segment'] = segment
    dataDict['program'] = program

    return render(request, 'segment_menu.html', dataDict)

    #NEW STUFF-----------------------------------------------------------------------------------------------







def action_menu(request, programId, segmentId):
    program_dict = fetch_program_data(programId)
    segment_dict = fetch_segment_data(segmentId)
    program_data = json.dumps(program_dict)
    segment_data = json.dumps(segment_dict)

    action_list = fetch_action_list(segmentId)
    formatted_action_list = format_action_list(action_list)  # make distinct and sort
    petition_url = get_petition_url(action_list)

    dataDict = {}
    dataDict['actionList'] = formatted_action_list
    dataDict['petitionURL'] = petition_url
    dataDict['programId'] = programId
    dataDict['programTitle'] = program_dict['programTitle']
    dataDict['programData'] = program_data

    dataDict['segmentId'] = segmentId
    dataDict['segmentTitle'] = segment_dict['segmentTitle']
    dataDict['purposeSummary'] = segment_dict['purposeSummary']
    dataDict['segmentData'] = segment_data

    return render(request, 'action_menu.html', dataDict)

def petition(request, programId, segmentId):
    redirect_url = "a"
    return HttpResponseRedirect(redirect_url)


# Twitter Verification and helper methods


    # def register(request):
    #
    #     # A boolean value for telling the template whether the registration was successful.
    #     # Set to False initially. Code changes value to True when registration succeeds.
    #     registered = False
    #
    #     # If it's a HTTP POST, we're interested in processing form data.
    #     if request.method == 'POST':
    #         # Attempt to grab information from the raw form information.
    #         # Note that we make use of both UserForm and UserProfileForm.
    #         user_form = UserForm(data=request.POST)
    #         profile_form = UserProfileForm(data=request.POST)
    #
    #         # If the two forms are valid...
    #         if user_form.is_valid() and profile_form.is_valid():
    #             # Save the user's form data to the database.
    #             user = user_form.save()
    #
    #             # Now we hash the password with the set_password method.
    #             # Once hashed, we can update the user object.
    #             user.set_password(user.password)
    #             user.save()
    #
    #             # Now sort out the UserProfile instance.
    #             # Since we need to set the user attribute ourselves, we set commit=False.
    #             # This delays saving the model until we're ready to avoid integrity problems.
    #             profile = profile_form.save(commit=False)
    #             profile.user = user
    #
    #             # Did the user provide a profile picture?
    #             # If so, we need to get it from the input form and put it in the UserProfile model.
    #             if 'picture' in request.FILES:
    #                 profile.picture = request.FILES['picture']
    #
    #             # Now we save the UserProfile model instance.
    #             profile.save()
    #
    #             # Update our variable to tell the template registration was successful.
    #             registered = True
    #
    #         # Invalid form or forms - mistakes or something else?
    #         # Print problems to the terminal.
    #         # They'll also be shown to the user.
    #         else:
    #             print user_form.errors, profile_form.errors
    #
    #     # Not a HTTP POST, so we render our form using two ModelForm instances.
    #     # These forms will be blank, ready for user input.
    #     else:
    #         user_form = UserForm()
    #         profile_form = UserProfileForm()
    #
    #     # Render the template depending on the context.
    #     return render(request,
    #             'registration_form.html',
    #             {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

    # def user_login(request):
    #
    #     # If the request is a HTTP POST, try to pull out the relevant information.
    #     if request.method == 'POST':
    #         # Gather the username and password provided by the user.
    #         # This information is obtained from the login form.
    #                 # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
    #                 # because the request.POST.get('<variable>') returns None, if the value does not exist,
    #                 # while the request.POST['<variable>'] will raise key error exception
    #         username = request.POST.get('username')
    #         password = request.POST.get('password')
    #
    #         # Use Django's machinery to attempt to see if the username/password
    #         # combination is valid - a User object is returned if it is.
    #         user = authenticate(username=username, password=password)
    #         print user
    #         # If we have a User object, the details are correct.
    #         # If None (Python's way of representing the absence of a value), no user
    #         # with matching credentials was found.
    #         if user:
    #             # Is the account active? It could have been disabled.
    #             if user.is_active:
    #                 # If the account is valid and active, we can log the user in.
    #                 # We'll send the user back to the homepage.
    #                 login(request, user)
    #                 return HttpResponseRedirect('/about/')
    #             else:
    #                 # An inactive account was used - no logging in!
    #                 return HttpResponse("Your Push Thought account is disabled.")
    #         else:
    #             # Bad login details were provided. So we can't log the user in.
    #             print "Invalid login details: {0}, {1}".format(username, password)
    #             return HttpResponse("Invalid login details supplied.")
    #
    #     # The request is not a HTTP POST, so display the login form.
    #     # This scenario would most likely be a HTTP GET.
    #     else:
    #         # No context variables to pass to the template system, hence the
    #         # blank dictionary object...
    #         return render(request, 'login.html', {})



