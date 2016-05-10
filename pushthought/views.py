from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.conf import settings
from django.contrib import messages

# from django.contrib.auth import authenticate, login
# from pushthought.forms import UserForm, UserProfileForm
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User

from django.contrib.sessions.models import Session

from .models import Program
from .models import Segment
from .models import MenuItem
from .forms import SegmentForm
from views_parse import *
# from django.contrib.auth import logout

import os
import tweepy
import json, httplib
import urllib


PARSE_APP_ID = 'lzb0o0wZHxbgyIHSyZLlooijAK9afoyN8RV4XwcM'
PARSE_REST_KEY = 'YTeYDL8DeSDNsmZT219Lp8iXgPZ24ZGu3ywUjo23'
TWITTER_CALLBACK_ROOT_URL = 'http://127.0.0.1:8000/verify_catch'
#TWITTER_CALLBACK_ROOT_URL = 'http://www.pushthought.com/verify_catch'

TWITTER_CONSUMER_KEY = settings.TWITTER_CONSUMER_KEY
TWITTER_CONSUMER_SECRET = settings.TWITTER_CONSUMER_SECRET

# import jsonpickle

# Create your views here.

def home(request):
    # userDict = dict()
    # userDict['users'] = User.objects.all()
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


# Use the login_required() decorator to ensure only those logged in can access the view.
# @login_required
def user_logout(request):
    # logout(request)

    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connection.connect()
    connection.request('POST', '/parse/logout', '', {
           "X-Parse-Application-Id": PARSE_APP_ID,
           "X-Parse-REST-API-Key": PARSE_REST_KEY,
           "X-Parse-Session-Token": request.session['sessionToken']
         })
    result = json.loads(connection.getresponse().read())
    try:
        del request.session['sessionToken']
    except:
        print "logout - no session token was available to delete"
    print "user is logged out"
    print result

    # Take the user back to the homepage.
    # return HttpResponseRedirect(reverse('my-named-url'))
    return HttpResponseRedirect('/home')

def api(request):
    obj = Program.objects.all()
    newObject = json.dumps(obj)
    return HttpResponse(newObject, content_type='application/json')

def get_user_in_parse_only(request, user_pk):

    try:
        session_token = request.session['sessionToken']
        print "session token in parse get user"
        print session_token
        connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
        connection.connect()
        connection.request('GET', '/parse/classes/_User/' + user_pk, '', {
               "X-Parse-Application-Id": PARSE_APP_ID,
               "X-Parse-REST-API-Key": PARSE_REST_KEY,
               "X-Parse-Session-Token": session_token
             })
        current_user = json.loads(connection.getresponse().read())
        print "Retrieved current user - behold:"
        print current_user
        return current_user
    except:
        print "This guy is not logged in"



def account_home(request, user_pk):

    from django.core.urlresolvers import reverse
    from django.shortcuts import redirect
    dataDict = {}
    try:
        session_token = request.session['sessionToken']
        print "session token top of account home:" + session_token
        current_user = get_user_in_parse_only(request, user_pk)
        dataDict['current_user'] = current_user
    except:
        print "no session token available on account home"
        print "no current user so redirecting to Sign In"
        return redirect(reverse('user_signin_form'))

    dataDict['user_pk'] = user_pk
    # programs = get_program_list()
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


# @login_required
def add_segment(request, user_pk, program_pk):
    program = get_object_or_404(Program, pk=program_pk)

    # A HTTP POST?
    if request.method == 'POST':
        form = SegmentForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return home(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = SegmentForm(initial={'program': program})

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'add_segment.html', {'form': form, 'program': program})


def contact(request):
    return render(request, 'contact.html')

    #NEW STUFF-----------------------------------------------------------------------------------------------





def user_signin_form(request):

    print "form request"
    print "currentUser"

    if request.method == 'POST':
        current_user = create_user(request)
        try:
            code = current_user['code']
            if current_user['code'] == 202:
                # User already exists, guide to login
                messages.info(request, 'Account already exists for this username.  Try logging in.')
                return render(request, 'user_signin_form.html')
        except:
            # User created, take to account_home
            messages.info(request, 'Success - you now have an account.')
            user_objectId = current_user['objectId']
            request.session['sessionToken'] = current_user['sessionToken']
            print "session token:" + request.session['sessionToken']
            account_home = "http://127.0.0.1:8000/account/" + user_objectId
            return HttpResponseRedirect(account_home)

            # return render(request, 'account_home.html',{'user_pk':current_user['objectId']})
    else:
        # Get request, send blank page
        return render(request, 'user_signin_form.html')


def login_form(request):

    print "login form request"

    if request.method == 'POST':
        current_user = login_user(request)
        try:
            code = current_user['code']
            if current_user['code'] == 101:
                messages.info(request, 'Invalid username/password')
                # User not found w email
                return render(request, 'login_form.html')
        except:
            # User created, take to account_home
            messages.info(request, 'Success: Logged In')
            user_objectId = current_user['objectId']
            request.session['sessionToken'] = current_user['sessionToken']
            print "session token:" + request.session['sessionToken']
            account_home = "http://127.0.0.1:8000/account/" + user_objectId
            return HttpResponseRedirect(account_home)

            # return render(request, 'account_home.html',{'user_pk':current_user['objectId']})
    else:
        # Get request, send blank page
        return render(request, 'login_form.html')



def program_detail(request,programId):
    segment_list = get_segment_list(programId)
    program_dict = fetch_program_data(programId)

    dataDict = {}
    dataDict['programDict'] = program_dict
    dataDict['segmentList'] = segment_list
    dataDict['programObjectId'] = program_dict['objectId']

    return render(request, 'program_detail.html',dataDict)

def get_segment_list(program_id):
    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    params = urllib.urlencode({"where":json.dumps({
            "programId":program_id
        }),
        "order":"-_created_at"})
    connection.connect()
    connection.request('GET','/parse/classes/Segments?%s' % params, '', {
        "X-Parse-Application-Id": PARSE_APP_ID,
        "X-Parse-REST-API-Key": PARSE_REST_KEY
    })
    segment_list = json.loads(connection.getresponse().read())
    return segment_list['results']

    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    params = urllib.urlencode({"where":json.dumps({
           "bioguideID": {
             "$in": bioguide_array
           }
         })})
    connection.connect()
    connection.request('GET', '/parse/classes/CongressImages?%s' % params, '', {
           "X-Parse-Application-Id": PARSE_APP_ID,
           "X-Parse-REST-API-Key": PARSE_REST_KEY
         })
def browse(request):
    program_list =  get_program_list()

    dataDict = {}
    dataDict['programList'] = program_list
    dataDict['segmentList'] = segment_list
    print (dataDict)

    import pprint
    pprint.pprint(dataDict)
    return render(request, 'browse.html', dataDict)

def get_program_list():

    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connection.connect()
    connection.request('GET','/parse/classes/Programs', '', {
        "X-Parse-Application-Id": PARSE_APP_ID,
        "X-Parse-REST-API-Key": PARSE_REST_KEY
    })

    program_list = json.loads(connection.getresponse().read())
    return program_list['results']

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

def get_petition_url(action_list):
    for item in action_list:
        if item['actionCategory'] == "Petition":
            petition_url = item['petitionURL']
    return petition_url


def fetch_segment_data(segment_id):
    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connection.connect()
    connection.request('GET','/parse/classes/Segments/'+ segment_id, '', {
        "X-Parse-Application-Id": PARSE_APP_ID,
        "X-Parse-REST-API-Key": PARSE_REST_KEY
    })
    segment_dict = json.loads(connection.getresponse().read())
    return segment_dict

def fetch_program_data(program_id):

    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connection.connect()
    connection.request('GET','/parse/classes/Programs/'+ program_id, '', {
        "X-Parse-Application-Id": PARSE_APP_ID,
        "X-Parse-REST-API-Key": PARSE_REST_KEY
    })
    program_dict = json.loads(connection.getresponse().read())
    return program_dict

def fetch_action_list(segment_id):
    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    params = urllib.urlencode({"where":json.dumps({
       "segmentId":segment_id
     })})
    connection.connect()
    connection.request('GET','/parse/classes/Messages?%s' % params, '', {
        "X-Parse-Application-Id": PARSE_APP_ID,
        "X-Parse-REST-API-Key": PARSE_REST_KEY
    })
    action_list = json.loads(connection.getresponse().read())
    return action_list['results']

def format_action_list(action_list):
    # extract actionCategory
    action_category_list = []
    for actionItem in action_list:
        action_category_list.append(actionItem['actionCategory'])

    # Make unique and sort
    unique_action_category_list = set(action_category_list)
    sorted_unique_action_category_list = sorted(unique_action_category_list)

    # Rearrange
    formattedList = move_to_front(sorted_unique_action_category_list,"Petition")
    formattedList = move_to_front(formattedList,"Regulator")
    formattedList = move_to_front(formattedList,"Local Representative")
    return formattedList

def move_to_front(list,value):
    indexNum = list.index(value)
    poppedItem = list.pop(indexNum)
    list.insert(0,poppedItem)
    return list


def get_congress_data(zipCode):
    root = "https://congress.api.sunlightfoundation.com/legislators/locate"
    apiKey = "ed7f6bb54edc4577943dcc588664c89f"

    urlAPI = root + "?zip=" + zipCode + "&apikey=" + apiKey

    import requests
    r = requests.get(urlAPI)
    #print r.status_code
    #print r.headers

    return json.loads(r.content)['results']

def add_congress_photos(congress_data,photo_data):
    print congress_data
    print photo_data
    for personItem in congress_data:
        for photoItem in photo_data:
            if str(personItem['bioguide_id']) == str(photoItem['bioguideID']):
                personItem['imageFileURL'] = photoItem['imageFile']['url']
    return congress_data


def get_congress_photos(congress_data):
    # create bioguide array from congress data (tells who we need photos for)
    bioguide_array = []
    for item in congress_data:
        bioguide_array.append(item['bioguide_id'])

    # Query for photos
    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    params = urllib.urlencode({"where":json.dumps({
           "bioguideID": {
             "$in": bioguide_array
           }
         })})
    connection.connect()
    connection.request('GET', '/parse/classes/CongressImages?%s' % params, '', {
           "X-Parse-Application-Id": PARSE_APP_ID,
           "X-Parse-REST-API-Key": PARSE_REST_KEY
         })
    photo_data = json.loads(connection.getresponse().read())
    return photo_data['results']

def add_title_and_full_name(congress_data_raw):
    for item in congress_data_raw:
        # Create full_name
        item['full_name'] = item['first_name'] + " " + item['last_name']
        # Create Title
        if item['title'] == "Rep":
            item['title'] = "Rep, " + item['state'] + " - d:" + str(item['district'])
        else:
            item['title'] = "Senator, " + item['state']
    return congress_data_raw


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

def get_hashtag_data(segmentId):
    # Query for hashtags
    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    params = urllib.urlencode({"where":json.dumps({
           "segmentObjectId":segmentId
         })})
    connection.connect()
    connection.request('GET', '/parse/classes/Hashtags?%s' % params, '', {
           "X-Parse-Application-Id": PARSE_APP_ID,
           "X-Parse-REST-API-Key": PARSE_REST_KEY
         })

    hashtag_data = json.loads(connection.getresponse().read())
    print "Hashtag data"
    print hashtag_data
    return hashtag_data['results']

def get_tweet_data(segmentId):

    # Query for tweets
    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    params = urllib.urlencode({
        "where":json.dumps({
            "segmentObjectId":segmentId,
            "messageType": "twitter"
        }),
        "order":"-_created_at"})
    connection.connect()
    connection.request('GET', '/parse/classes/sentMessages?%s' % params, '', {
           "X-Parse-Application-Id": PARSE_APP_ID,
           "X-Parse-REST-API-Key": PARSE_REST_KEY
         })

    tweet_data = json.loads(connection.getresponse().read())
    print "Tweet data"
    print tweet_data
    return tweet_data['results']


def petition(request, programId, segmentId):



    redirect_url = "a"
    return HttpResponseRedirect(redirect_url)


# Twitter Verification and helper methods
def verify_twitter(request, programId, segmentId, tweet):
    print "ajax hitting verify twitter!"
    tweet_text = urllib.unquote_plus(tweet)
    #request.session['user_object_id'] = 'JMSR6hFydj'
    try:
        print "user has token, user id:" + request.session['user_object_id']
    except:
        print "no user object in session"

    try:
        print "TRYING"
        user_object_id = str(request.session['user_object_id'])
        current_user = get_parse_user_with_twitter_auth(user_object_id)

        # Gather twitter keys -> methods below
        twitter_keys = { "auth_token" : current_user['authData']['twitter']['auth_token'],
                         "auth_token_secret" : current_user['authData']['twitter']['auth_token_secret'] }
        twitter_screen_name = current_user['authData']['twitter']['screen_name']

        # Send tweet and show success
        send_tweet_with_tweepy(tweet_text, twitter_keys)
        show_tweet_success_message(request, tweet_text)

        # Save tweet action
        action_object_id = save_tweet_action(request,tweet_text,current_user,twitter_screen_name)

        # Save #'s
        save_hashtags(request,tweet_text,current_user,twitter_screen_name,action_object_id)

        # Save @'s
        save_targets(request,tweet_text,current_user,twitter_screen_name, action_object_id)

        # Update SegmentStats
        update_segment_stats(request)

        # Post-tweet navigation
        if 'last_menu_url' in request.session:
            source_action_menu = request.session['last_menu_url']
            return HttpResponseRedirect(source_action_menu)
        else:
            return render(request, 'home.html')

    except:
        print "exception"
        CALLBACK_URL = TWITTER_CALLBACK_ROOT_URL

        # App level auth
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, CALLBACK_URL)
        redirect_url = auth.get_authorization_url()

        # Store session value b/c sending to twitter for auth
        request.session['request_token'] = auth.request_token
        request.session['tweetText'] = tweet_text
        request.session['programId'] = programId
        request.session['segmentId'] = segmentId
        request.session.modified = True

        return HttpResponseRedirect(redirect_url)

def get_parse_user_with_twitter_auth(user_object_id):

    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    params = urllib.urlencode({"keys":"_auth_data_twitter"})
    connection.connect()
    connection.request('GET', '/parse/classes/_User/' + user_object_id + '?%s' % params, '', {
           "X-Parse-Application-Id": PARSE_APP_ID,
           "X-Parse-REST-API-Key": PARSE_REST_KEY
         })
    current_user = json.loads(connection.getresponse().read())
    print "parse user info"
    print current_user
    return current_user


def retrieve_twitter_key(user_object_id): #helper

    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    params = urllib.urlencode({"keys":"_auth_data_twitter"})
    connection.connect()
    connection.request('GET','/parse/classes/_User/'+ user_object_id + '?%s' % params, '', {
        "X-Parse-Application-Id": PARSE_APP_ID,
        "X-Parse-REST-API-Key": PARSE_REST_KEY
    })
    twitter_key = json.loads(connection.getresponse().read())
    return twitter_key

def send_tweet_with_tweepy(tweet_text,twitter_keys): #helper
    auth_token = twitter_keys['auth_token']
    auth_token_secret = twitter_keys['auth_token_secret']
    CALLBACK_URL = TWITTER_CALLBACK_ROOT_URL
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, CALLBACK_URL)
    auth.set_access_token(auth_token, auth_token_secret)

    api = tweepy.API(auth)
    api.update_status(tweet_text)
    print "tweet sent"
    return None

def show_tweet_success_message(request, tweet_text): #helper
    #send success message
    messages.success(request, 'Tweet sent successfully.')
    # response = JsonResponse({'tweet_text': tweet_text})
    return None


def verify_catch(request):

    print "verify catch starting"

    # Establish auth connection using Ap identification
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)

    # Get Request Token, then delete from session
    token = request.session['request_token']
    print "request token being used" + str(token)
    auth.request_token = token
    try:
        del request.session['request_token']
        print "deleting request token"
    except request.exceptions.HTTPError as e:
        print "And you get an HTTPError:", e.message

    # Get Access Key
    verifier = request.GET.get('oauth_verifier')
    accessKey = auth.get_access_token(verifier)
    accessKeyToken = accessKey[0]
    accessKeyTokenSecret = accessKey[1]

    # Establish API connection
    api = tweepy.API(auth)

    # Get Twitter User info
    twitter_user = api.me()
    twitter_screen_name = twitter_user.screen_name


    current_user = log_user_into_parse(twitter_user,accessKeyToken,accessKeyTokenSecret)
    update_user_with_twitter_data (current_user,twitter_user,accessKeyToken,accessKeyTokenSecret)

    request.session['user_object_id'] = str(current_user['objectId'])


    # Send tweet (if available)
    if 'tweetText' in request.session:
        tweet_text = request.session['tweetText']
        del request.session['tweetText']
        api.update_status(tweet_text)
        show_tweet_success_message(request, tweet_text)
        print "tweet sent"

        # Save tweet action
        action_object_id = save_tweet_action(request,tweet_text,current_user,twitter_screen_name)

        # Save #'s
        save_hashtags(request,tweet_text,current_user,twitter_screen_name,action_object_id)

        # Save @'s
        save_targets(request,tweet_text,current_user,twitter_screen_name, action_object_id)

        # Save to SegmentStats
        update_segment_stats(request)





        request.session.modified = True
        
    else:
        print "verify catch NO message to send"

    # Navigation
    if 'last_menu_url' in request.session:
        source_url = request.session['last_menu_url']

        return HttpResponseRedirect(source_url)
        # return render(request, 'fed_rep_action_menu.html', {'programId'z: program, 'segmentId': segment})
    else:
        return render(request, 'home.html')


def save_tweet_action(request,tweet_text,current_user,twitter_screen_name): #helper
    connectionTweet = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connectionTweet.connect()
    connectionTweet.request('POST', '/parse/classes/sentMessages', json.dumps({
        "messageText": tweet_text,
        "actionCategory": "Local Representative",
        "messageCategory": "Local Representative",
        "messageType": "twitter",
        "userObjectId": current_user['objectId'],
        "twitterUserName": twitter_screen_name,
        "programObjectId" : request.session['programId'],
        "segmentObjectId" : request.session['segmentId']
        }), {
        "X-Parse-Application-Id": PARSE_APP_ID,
        "X-Parse-REST-API-Key": PARSE_REST_KEY,
        "Content-Type": "application/json"
    })
    result = json.loads(connectionTweet.getresponse().read())
    action_object_id = result['objectId']
    return action_object_id


def save_hashtags(request,tweet_text,current_user,twitter_screen_name,action_object_id):
    hashtag_list = set([i[1:] for i in tweet_text.split() if i.startswith("#")])

    for hashtag in hashtag_list:
        #search result for it
                #found exit and add one
                #move on to next
        connectionTweet = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
        connectionTweet.connect()
        connectionTweet.request('POST', '/parse/classes/Hashtags', json.dumps({
            "hashtag" : hashtag,
            "frequency" : "1",
            "messageText": tweet_text,
            "actionCategory": "Local Representative",
            "messageCategory": "Local Representative",
            "messageType": "twitter",
            "userObjectId": current_user['objectId'],
            "twitterUserName": twitter_screen_name,
            "programObjectId" : request.session['programId'],
            "segmentObjectId" : request.session['segmentId'],
            'actionObjectId' : action_object_id
            }), {
            "X-Parse-Application-Id": PARSE_APP_ID,
            "X-Parse-REST-API-Key": PARSE_REST_KEY,
            "Content-Type": "application/json"
        })
        result = json.loads(connectionTweet.getresponse().read())
        print "hashtag save result"
        print result
    return None


def save_targets(request,tweet_text,current_user,twitter_screen_name,action_object_id):
    target_list = set([i[1:] for i in tweet_text.split() if i.startswith("@")])

    for target in target_list:

        connectionTweet = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
        connectionTweet.connect()
        connectionTweet.request('POST', '/parse/classes/TargetTwitterNames', json.dumps({
            "targetTwitterName" : target,
            "frequency" : 1,
            "messageText": tweet_text,
            "actionCategory": "Local Representative",
            "messageCategory": "Local Representative",
            "messageType": "twitter",
            "userObjectId": current_user['objectId'],
            "twitterUserName": twitter_screen_name,
            "programObjectId" : request.session['programId'],
            "segmentObjectId" : request.session['segmentId'],
            'actionObjectId' : action_object_id
            }), {
            "X-Parse-Application-Id": PARSE_APP_ID,
            "X-Parse-REST-API-Key": PARSE_REST_KEY,
            "Content-Type": "application/json"
        })
        result = json.loads(connectionTweet.getresponse().read())
        print "address save result"
        print result
    return None

def update_segment_stats(request):
    # NEED TO ADD LOGIC TO ADD IF NOT THERE

    #look up value
    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    params = urllib.urlencode({"where":json.dumps({
       "segmentObjectId": request.session['segmentId']
     })})
    connection.connect()
    connection.request('GET', '/parse/classes/SegmentStats?%s' % params, '', {
       "X-Parse-Application-Id": PARSE_APP_ID,
       "X-Parse-REST-API-Key": PARSE_REST_KEY
     })
    result = json.loads(connection.getresponse().read())
    print "downloaded segment stats"
    print result

    result_dict = result['results']
    print "result dict"
    print result_dict
    action_count = result_dict[0]['actionCount']
    action_count = action_count + 1

    #update entry
    connection2 = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connection2.connect()
    connection2.request('PUT', '/parse/classes/SegmentStats/' + result_dict[0]['objectId'] , json.dumps({
           "actionCount": action_count
         }), {
           "X-Parse-Application-Id": PARSE_APP_ID,
           "X-Parse-REST-API-Key": PARSE_REST_KEY,
           "Content-Type": "application/json"
         })

    result2 = connection2.getresponse().read()
    print "uploaded segment stats"

    print result2
    return None


def log_user_into_parse(twitter_user,access_key_token,access_key_token_secret): #helper
    #sign up/log in user linked to twitter, save access keys
    import json,httplib
    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connection.connect()
    connection.request('POST', '/parse/classes/_User', json.dumps({
       "authData": {
         "twitter": {
           "id": twitter_user.id,
           "screen_name": twitter_user.screen_name,
           "consumer_key": TWITTER_CONSUMER_KEY,
           "consumer_secret": TWITTER_CONSUMER_SECRET,
           "auth_token": access_key_token,
           "auth_token_secret": access_key_token_secret
         }
       }
     }), {
       "X-Parse-Application-Id": PARSE_APP_ID,
       "X-Parse-REST-API-Key": PARSE_REST_KEY,
       "X-Parse-Revocable-Session": "1",
       "Content-Type": "application/json"
    })
    result = json.loads(connection.getresponse().read())
    print result
    print 'session TOKEN:' + str(result['sessionToken'])

    return result

def update_user_with_twitter_data(current_user,twitter_user,access_key_token,access_key_token_secret): #helper

    # Update the user info always, new and old users
    # update user information with Session token
    import json,httplib
    connection2 = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connection2.connect()
    connection2.request('PUT', '/parse/classes/_User/' + str(current_user['objectId']), json.dumps({
        "name_tw": twitter_user.name,
        "id_tw": twitter_user.id_str,
        "followers_count_tw": twitter_user.followers_count,
        "friends_count_tw": twitter_user.friends_count,
        "location_tw": twitter_user.location,
        "time_zone_tw": twitter_user.time_zone,
        "url_tw": twitter_user.url,
        "session_token_parse" : current_user['sessionToken'],
        "twitter_token" : access_key_token,
        "twitter_token_secret" : access_key_token_secret
    }), {
        "X-Parse-Application-Id": PARSE_APP_ID,
        "X-Parse-REST-API-Key": PARSE_REST_KEY,
        "X-Parse-Session-Token": current_user['sessionToken'],
        "Content-Type": "application/json"
    })
    result = json.loads(connection2.getresponse().read())
    print "updated Parse user with Twitter Data"

    return None




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



