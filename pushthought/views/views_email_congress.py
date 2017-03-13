from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.conf import settings
from django.template import RequestContext


from views_alerts import *
from views_api import *
from views_get_data import *
from views_congress import *
from views_parse_user import *
from views_twtitter_auth import *
from views_user_forms import *

# from django.contrib.auth import logout

import tweepy
import json, httplib
import pymongo

PARSE_APP_ID = settings.PARSE_APP_ID
PARSE_REST_KEY = settings.PARSE_REST_KEY
TWITTER_CALLBACK_ROOT_URL = settings.TWITTER_CALLBACK_ROOT_URL
# TWITTER_CALLBACK_ROOT_URL = 'http://www.pushthought.com/verify_catch'

TWITTER_CONSUMER_KEY = settings.TWITTER_CONSUMER_KEY
TWITTER_CONSUMER_SECRET = settings.TWITTER_CONSUMER_SECRET

MONGODB_URI = settings.MONGODB_URI

 # This top view is exposed on the urls page.
def get_congress_email_fields(request):
    bioguideId = request.body
    print "bioguideId:", bioguideId

    result = get_congress_required_fields(bioguideId)
    if len(result) > 0:
        print "congress req fields in database, returning from parse-server"
        resultFields = result[0]['required_fields']
        return HttpResponse(json.dumps(resultFields), content_type="application/json")
    else:
        print "No congress required fields in DB so pulling from phantom congress"
        connection = httplib.HTTPSConnection('congressforms.eff.org')
        connection.connect()
        connection.request('POST', '/retrieve-form-elements/',
            json.dumps({
                "bio_ids": [bioguideId],
            }),
            {#headers
               "Content-Type": "application/json"
            })
        required_fields_object = json.loads(connection.getresponse().read())
        save_fields(bioguideId, required_fields_object)
        result = get_congress_required_fields(bioguideId)
        return HttpResponse(json.dumps(result), content_type="application/json")

def get_congress_required_fields(bioguideId):
    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connection.connect()
    params = urllib.urlencode({"where":json.dumps({
           "bioguideId": bioguideId
         })})
    connection.request('GET', '/parse/classes/CongressRequiredEmailFields?%s' % params,
                       '',
                       {
                           "X-Parse-Application-Id": PARSE_APP_ID,
                           "X-Parse-REST-API-Key": PARSE_REST_KEY,
                           "Content-Type": "application/json"
                       })
    result = json.loads(connection.getresponse().read())
    print "pulling required fields result", result['results']
    return result['results']


def save_fields(bioguideId, required_fields_object):
    print "fields_array before savew:::::::::::", required_fields_object
    required_fields = required_fields_object[bioguideId]["required_actions"]

    for field in required_fields:
        field['value'] = field['value'].replace('$','')
        if field['value'] == 'NAME_PREFIX':
            print "AAAAAA FOUND PREFIX"
            optionDict = field['options_hash']
            for item in optionDict:
                print "item:", type(item)
                for i in item:
                    if i == '.':
                        print "YES YES YES"
                        i = ''
                    print "new item:", i

        if field['value'] == 'TOPIC':
            optionDict = field['options_hash']
            try:
                for key, value in optionDict.items():
                    newKey = key.replace('.', '').replace('   ',' ').replace('/', '').replace(',', '').replace('$','')
                    print key
                    print newKey
                    optionDict[newKey] = optionDict.pop(key)
            except:
                for item in optionDict:
                    newItem = item.replace('.', '').replace('   ', ' ').replace('/', '').replace(',', '').replace('$','')
                    item = newItem

    print "after replace::::::::::::", required_fields

    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connection.connect()
    connection.request('POST', '/parse/classes/CongressRequiredEmailFields',
    json.dumps({
        "bioguideId": bioguideId,
        "required_fields": required_fields
    }),
   {
       "X-Parse-Application-Id": PARSE_APP_ID,
       "X-Parse-REST-API-Key": PARSE_REST_KEY,
       "Content-Type": "application/json"
   })
    result = json.loads(connection.getresponse().read())
    print "save result for required fields::::::", result
    return HttpResponse(json.dumps(result), content_type="application/json")

def submit_congress_email(request):
    print request.body
    bodyString = request.body

    print "submitting email to congressperson"
    connection = httplib.HTTPSConnection('congressforms.eff.org')
    # connection = httplib.HTTPSConnection('ptparse.herokuapp.com')
    connection.connect()
    connection.request('POST', '/fill-out-form/',bodyString,
                       {  # headers
                           "Content-Type": "application/json"
                       })
    send_response_object = json.loads(connection.getresponse().read())
    return send_response_object

def submit_congress_captcha(request):
    print request.body

    bodyString = request.body

    dict = {}
    j = json.loads(bodyString)
    dict['answer'] = j['answer']
    dict['uid'] = j['uid']
    dictString = json.dumps(dict)


    print "submitting captcha"
    connection = httplib.HTTPSConnection('congressforms.eff.org')
    # connection = httplib.HTTPSConnection('ptparse.herokuapp.com')
    connection.connect()
    connection.request('POST', '/fill-out-captcha/', dictString,
                       {  # headers
                           "Content-Type": "application/json"
                       })
    captcha_response_object = json.loads(connection.getresponse().read())
    return captcha_response_object


def captcha_crush(request, send_response_object):
    bioguideId = request.body['bio_id']
    url = request.body['url']
    uid = request.body['uid']



    return HttpResponse(json.dumps(send_response_object), content_type="application/json")