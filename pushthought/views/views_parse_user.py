from django.conf import settings
import urllib, httplib, json
from django.http import HttpResponseRedirect
TWITTER_CALLBACK_ROOT_URL = settings.TWITTER_CALLBACK_ROOT_URL


TWITTER_CONSUMER_KEY = settings.TWITTER_CONSUMER_KEY
TWITTER_CONSUMER_SECRET = settings.TWITTER_CONSUMER_SECRET

PARSE_APP_ID = settings.PARSE_APP_ID
PARSE_REST_KEY = settings.PARSE_REST_KEY

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
        print "Retrieved current user - behold:", current_user
        return current_user
    except:
        print "This guy is not logged in"

#helper
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

#helper
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


# helper
def log_user_into_parse(twitter_user,access_key_token,access_key_token_secret): #helper
    #sign up/log in user linked to twitter, save access keys
    print "login data"
    print twitter_user

    import json,httplib
    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connection.connect()
    connection.request('POST', '/parse/classes/_User', json.dumps({
       "authData": {
         "twitter": {
           "id": twitter_user.id,
           "screen_name": twitter_user.screen_name,
           "consumer_key": settings.TWITTER_CONSUMER_KEY,
           "consumer_secret": settings.TWITTER_CONSUMER_SECRET,
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
    print "result log_user_into_parse", result
    # print 'session TOKEN:' + str(result['sessionToken'])

    return result



def login_user(request):
    print "login user method"
    print request.POST
    user_name = request.POST['user_email']
    password = request.POST['password']
    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    params = urllib.urlencode({"username":user_name,"password": password})
    connection.connect()
    connection.request('GET', '/parse/login?%s' % params, '', {
           "X-Parse-Application-Id": PARSE_APP_ID,
           "X-Parse-REST-API-Key": PARSE_REST_KEY,
           "X-Parse-Revocable-Session": "1"
         })
    result = json.loads(connection.getresponse().read())
    print "printing result of login:"
    print result

    return result

#helper
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

import json,httplib, urllib
from django.contrib import messages

def create_user(request):
    print "Create user method"
    print request.POST
    user_email = request.POST['user_email']
    user_password = request.POST['password']

    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connection.connect()
    connection.request('POST', '/parse/classes/_User', json.dumps({
           "username": user_email,
           "password": user_password
         }), {
           "X-Parse-Application-Id": PARSE_APP_ID,
           "X-Parse-REST-API-Key": PARSE_REST_KEY,
           "X-Parse-Revocable-Session": "1",
           "Content-Type": "application/json"
         })
    result = json.loads(connection.getresponse().read())

    print "print callback value for user creation."
    print result

    return result