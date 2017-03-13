from django.conf import settings
import urllib, httplib, json
from django.http import HttpResponseRedirect, HttpResponse
TWITTER_CALLBACK_ROOT_URL = settings.TWITTER_CALLBACK_ROOT_URL


TWITTER_CONSUMER_KEY = settings.TWITTER_CONSUMER_KEY
TWITTER_CONSUMER_SECRET = settings.TWITTER_CONSUMER_SECRET
PARSE_MASTER = settings.PARSE_MASTER

PARSE_APP_ID = settings.PARSE_APP_ID
PARSE_REST_KEY = settings.PARSE_REST_KEY

# def get_session_token(objectId)

def get_user_by_twitter_screen_name(request, twitter_screen_name):
    print "looking up user by twitter name:", twitter_screen_name
    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connection.connect()
    params = urllib.urlencode({
        "include": "tokenSession, twitterScreenName",
        "where":json.dumps({
            "twitterScreenName": twitter_screen_name
        })
    });
    connection.request('GET', '/parse/classes/_User/' + '?%s' % params, '', {
       "X-Parse-Application-Id": PARSE_APP_ID,
       "X-Parse-REST-API-Key": PARSE_REST_KEY,
        "X-Parse-Master-Key": PARSE_MASTER
     })
    results = json.loads(connection.getresponse().read())

    try:
        current_user = results['results'][0]
    except:
        current_user = None

    # save sessionToken to session
    if current_user:
        request.session['sessionToken'] = current_user['tokenSession']
        print "tokenSession entered:", request.session['sessionToken']
        request.session['userObjectId'] = current_user['objectId']
        print "userObjectId entered:", request.session['userObjectId']
        request.session.modified = True

    return current_user

def create_user_with_twitter_auth(request, twitter_user,access_key_token,access_key_token_secret):


    # user data into save dictionary
    jsonDict = {
        "username": str(twitter_user.screen_name),
        "twitterScreenName": str(twitter_user.screen_name),
        "password": "password"
    }

    # if zip, add it to dictionary
    try:
        zip = request.session['zip']
        jsonDict['zip'] = zip
    except:
        print "zip not in session so zip not saved with created user."

    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connection.connect()
    connection.request('POST', '/parse/classes/_User', json.dumps(jsonDict),
    {
        "X-Parse-Application-Id": PARSE_APP_ID,
        "X-Parse-REST-API-Key": PARSE_REST_KEY,
        "X-Parse-Revocable-Session": "1",
        "Content-Type": "application/json"
    })
    current_user = json.loads(connection.getresponse().read())

    # save sessionToken to session
    print "saving sessionToken into session from created user"
    request.session['sessionToken'] = current_user['sessionToken']
    request.session['userObjectId'] = current_user['objectId']
    print "sessionToken here entered:", request.session['sessionToken']
    print "userObjectId  here entered:", request.session['userObjectId']
    request.session.modified = True

    #save session Tokens to user
    connection2 = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connection2.connect()
    connection2.request('PUT', '/parse/classes/_User/' + current_user['objectId'], json.dumps({
        "sessionToken": request.session['sessionToken'],
        "tokenSession": request.session['sessionToken']

    }),
    {
       "X-Parse-Application-Id": PARSE_APP_ID,
       "X-Parse-REST-API-Key": PARSE_REST_KEY,
       "X-Parse-Session-Token": request.session['sessionToken'],
       "Content-Type": "application/json"
    })
    result2 = json.loads(connection2.getresponse().read())
    if result2:
        print "sessionToken updated to user:", result2
    else:
        print "error updating sessionToken to user"

    return current_user

def update_user_with_twitter_profile_data(request, current_user,twitter_user,access_key_token,access_key_token_secret):
    data = twitter_user.__dict__
    twitter_user_dictionary = data
    # print twitter_user_dictionary
    print type(str(access_key_token))
    print type(access_key_token_secret)

    authDic = json.dumps({
        "sessionToken": request.session['sessionToken'],
        "tokenSession": request.session['sessionToken'],
        "name_tw": twitter_user.name,
        "id_tw": twitter_user.id_str,
        "followers_count_tw": twitter_user.followers_count,
        "friends_count_tw": twitter_user.friends_count,
        "location_tw": twitter_user.location,
        "time_zone_tw": twitter_user.time_zone,
        "url_tw": twitter_user.url,
        "twitter_user": str(twitter_user_dictionary),
        "authData": {
            "twitter": {
                "id": twitter_user.id,
                "screen_name": twitter_user.screen_name,
                "auth_token": access_key_token,
                "auth_token_secret": access_key_token_secret
             }
         }
    })

    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connection.connect()
    connection.request('PUT', '/parse/classes/_User/' + current_user['objectId'], authDic,
    {
       "X-Parse-Application-Id": PARSE_APP_ID,
       "X-Parse-REST-API-Key": PARSE_REST_KEY,
       "X-Parse-Session-Token": request.session['sessionToken'],
       "Content-Type": "application/json"
    })
    result = json.loads(connection.getresponse().read())
    if result:
        print "twitter profile updated to user successfully:"
    else:
        print "error updating twitter profile info to user"
    return None



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
    print "twitter user in login method", twitter_user

    import json,httplib
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('GET', '/1/_User/g7y9tkhB7O', '', {
       "X-Parse-Application-Id": "${APPLICATION_ID}",
       "X-Parse-REST-API-Key": "${REST_API_KEY}"
     })
    result = json.loads(connection.getresponse().read())
    print result


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