from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.conf import settings
from django.contrib import messages


# from django.contrib.auth import authenticate, login
# from pushthought.forms import UserForm, UserProfileForm
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.contrib.sessions.models import Session

from .models import Program
from .models import Segment
from .models import MenuItem
from .forms import SegmentForm

import json
import tweepy

import os

PARSE_APP_ID = 'lzb0o0wZHxbgyIHSyZLlooijAK9afoyN8RV4XwcM'
PARSE_REST_KEY = 'YTeYDL8DeSDNsmZT219Lp8iXgPZ24ZGu3ywUjo23'

# import jsonpickle

# Create your views here.

def home(request):
    # userDict = dict()
    # userDict['users'] = User.objects.all()
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def api(request):
    obj = Program.objects.all()
    newObject = json.dumps(obj)
    return HttpResponse(newObject, content_type='application/json')


# @login_required
def account_home(request, user_pk):
    programs = Program.objects.filter(user=user_pk)
    dataDict = {}
    dataDict['user_pk'] = user_pk
    dataDict['programs'] = programs

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


def fed_rep_action_menu(request, programId, segmentId):

    source_url = request.build_absolute_uri()

    print "source" + source_url
    request.session['last_menu_url'] = source_url
    request.session['programId'] = programId
    request.session['segmentId'] = segmentId
    print "session:(last url)" + request.session['last_menu_url']
    print "Fed Action menu end"

    return render(request, 'fed_rep_action_menu.html', {'programId': programId, 'segmentId': segmentId})


def verify_twitter(request):

    import json,httplib
    TWITTER_CONSUMER_KEY = settings.TWITTER_CONSUMER_KEY
    TWITTER_CONSUMER_SECRET = settings.TWITTER_CONSUMER_SECRET

    print "ajax hitting verify twitter!"
    print request
    print request.POST
    print "request dumps body"
    print request.body
    tweetText = request.POST['tweetText'] # if 'user_object_id' in request.session:

    try:
        user_object_id = request.session['user_object_id']

        connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
        connection.connect()
        connection.request('GET', '/1/users/' + user_object_id, '', {
            "X-Parse-Application-Id": PARSE_APP_ID,
            "X-Parse-REST-API-Key": PARSE_REST_KEY
        })

        currentUser = json.loads(connection.getresponse().read())
        auth_token = currentUser.auth_token
        auth_token_secret = currentUser.auth_token_secret
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_access_token(auth_token, auth_token_secret)


        api = tweepy.API(auth)
        api.update_status(tweetText)
        print "tweet sent"
        messages.success(request, 'Tweet sent successfully.')
        response = JsonResponse({'tweetText': tweetText})
        print "end of try"
        return response
    except:
        print "exception"
        CALLBACK_URL = 'http://www.pushthought.com/verify_catch'
        # CALLBACK_URL = 'http://127.0.0.1:8000/verify_catch'

        # App level auth
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, CALLBACK_URL)
        redirect_url = auth.get_authorization_url()

        return HttpResponseRedirect(redirect_url)



    #         send to verify page
    # else:
    #     redirect_url = auth.get_authorization_url()
    #     return HttpResponseRedirect(redirect_url)

    #get current user (parse) to pull twitter tokens


    #is this twitter user already signed in with me
    #is there sesssion with twitter token?
    #is there a user for Parse, with token?

    # Check if we have twitter token, if so then send
    # update the parse user info after send, always

    # print json.dumps(request.POST, indent=4, sort_keys=True)

    # print "verify twitter no message"
    # CALLBACK_URL = 'http://127.0.0.1:8000/verify_catch'
    # TWITTER_CONSUMER_KEY = settings.TWITTER_CONSUMER_KEY
    # TWITTER_CONSUMER_SECRET = settings.TWITTER_CONSUMER_SECRET
    #
    # # App level auth
    # auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, CALLBACK_URL)
    # redirect_url = auth.get_authorization_url()
    # request.session['request_token'] = auth.request_token



def verify_twitter_with_tweet(request, tweet_text):
    print "verify twitter with message"

    CALLBACK_URL = 'http://127.0.0.1:8000/verify_catch/'
    print CALLBACK_URL

    TWITTER_CONSUMER_KEY = settings.TWITTER_CONSUMER_KEY
    TWITTER_CONSUMER_SECRET = settings.TWITTER_CONSUMER_SECRET

    # App level auth
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, CALLBACK_URL)
    redirect_url = auth.get_authorization_url()

    # store data in session
    request.session['request_token'] = auth.request_token
    request.session['tweet_text'] = tweet_text

    return HttpResponseRedirect(redirect_url)


def verify_catch(request):

    TWITTER_CONSUMER_KEY = settings.TWITTER_CONSUMER_KEY
    TWITTER_CONSUMER_SECRET = settings.TWITTER_CONSUMER_SECRET

    # Establish auth connection using Ap identification
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)

    # Get Request Token, then delete from session
    token = request.session['request_token']
    auth.request_token = token
    try:
        del request.session['request_token']
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
    twitterUser = api.me()


    #sign up/log in user linked to twitter, save access keys
    import json,httplib
    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connection.connect()
    connection.request('POST', '/parse/classes/_User', json.dumps({
       "authData": {
         "twitter": {
           "id": twitterUser.id,
           "screen_name": twitterUser.screen_name,
           "consumer_key": TWITTER_CONSUMER_KEY,
           "consumer_secret": TWITTER_CONSUMER_SECRET,
           "auth_token": accessKeyToken,
           "auth_token_secret": accessKeyTokenSecret
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

    request.session['user_object_id'] = str(result['objectId'])

    currentUser = result

    # Update the user info always, new and old users
    # update user information with Session token
    import json,httplib
    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connection.connect()
    connection.request('PUT', '/parse/classes/_User/' + str(currentUser['objectId']), json.dumps({
        "name_tw": twitterUser.name,
        "id_tw": twitterUser.id_str,
        "followers_count_tw": twitterUser.followers_count,
        "friends_count_tw": twitterUser.friends_count,
        "location_tw": twitterUser.location,
        "time_zone_tw": twitterUser.time_zone,
        "url_tw": twitterUser.url,
        "session_token_parse" : currentUser['sessionToken']
    }), {
        "X-Parse-Application-Id": PARSE_APP_ID,
        "X-Parse-REST-API-Key": PARSE_REST_KEY,
        "X-Parse-Session-Token": currentUser['sessionToken'],
        "Content-Type": "application/json"
    })
    result2 = json.loads(connection.getresponse().read())
    print "after SAVE"
    print result2

    # Send tweet (if available)
    if 'tweet_text' in request.session:
        tweetText = request.session['tweet_text']
        del request.session['tweet_text']
        api.update_status(tweetText)
        print "tweet sent"
        messages.success(request, 'Tweet sent successfully.')

        # CREATE and SAVE the Action
        connectionTweet = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
        connectionTweet.connect()
        connectionTweet.request('POST', '/parse/classes/sentMessages', json.dumps({
            "messageText": tweetText,
            "actionCategory": "Local Representative",
            "messageCategory": "Local Representative",
            "messageType": "twitter",
            "userObjectId": currentUser['objectId'],
            "twitterUserName": twitterUser.name
            # "segmentObjectId":,
            # "programObjectId":

            }), {
            "X-Parse-Application-Id": PARSE_APP_ID,
            "X-Parse-REST-API-Key": PARSE_REST_KEY,
            "Content-Type": "application/json"
        })

        result = json.loads(connection.getresponse().read())
    else:
        print "verify catch NO message to send"


    if 'last_menu_url' in request.session:
        source_url = request.session['last_menu_url']

        return HttpResponseRedirect(source_url)
        # return render(request, 'fed_rep_action_menu.html', {'programId'z: program, 'segmentId': segment})
    else:
        return render(request, 'home.html')



    # #create new user in using parse-server API
    # import json,httplib
    # connection = httplib.HTTPSConnection('ptparse.herokuapp.com',443)
    # connection.connect()
    # connection.request('POST', '/parse/classes/_User', json.dumps({
    #    "username": twitterUser.screen_name,
    #    "password": "twitter"
    #  }), {
    #    "X-Parse-Application-Id": "lzb0o0wZHxbgyIHSyZLlooijAK9afoyN8RV4XwcM",
    #    "X-Parse-REST-API-Key": "YTeYDL8DeSDNsmZT219Lp8iXgPZ24ZGu3ywUjo23",
    #    "X-Parse-Revocable-Session": "1",
    #    "Content-Type": "application/json"
    #  }
    # )
    # result = connection.getresponse()
    # theResult = json.loads(result.read().decode())
    # print result
    # print theResult
    #
    # try:
    #     print theResult['code']
    #     print theResult['error']
    # except KeyError:
    #     print 'key error exception silenced, user save verify_catch'

    #  Get Tweet Text if exists and Send





def action_menu(request, programId, segmentId):
    program = programId
    segment = segmentId


    return render(request, 'action_menu.html', {'programId': program, 'segmentId': segment})


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


    # from django.contrib.auth import logout
    #
    # # Use the login_required() decorator to ensure only those logged in can access the view.
    # # @login_required
    # def user_logout(request):
    #     # Since we know the user is logged in, we can now just log them out.
    #     logout(request)
    #
    #     # Take the user back to the homepage.
    #     return HttpResponseRedirect('/home/')
