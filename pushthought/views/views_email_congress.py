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
from views_email_congress_format_email_fields import *

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

def get_congress_email_fields(bioguideArray):
    print bioguideArray
    field_list_objects = get_congress_required_fields_parse(bioguideArray)
    missing_bioguides = get_missing_bioguides(bioguideArray,field_list_objects)
    if len(missing_bioguides)>0:
        phantom_required_objects = get_congress_email_fields_phantom(missing_bioguides)
        save_failures(missing_bioguides,phantom_required_objects)
        for item in phantom_required_objects:
            field_list_objects.append(item)

    print "Finally here!, all concatenated:",field_list_objects
    master_field_list = create_master_field_list(field_list_objects)
    return master_field_list

def save_failures(missing_bioguides,phantom_required_objects):
    failures_array = []

    for item in missing_bioguides:
        found = False
        for item2 in phantom_required_objects['results']:
            print item2
            if item == item2['bioguideId']:
                found = True
        if not found:
            failures_array.append(item)
    print "not in phantom_array", failures_array

    for item2 in failures_array:
        connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
        connection.connect()
        connection.request('POST', '/parse/classes/CongressEmailFieldsUpdateLog',
                           json.dumps({
                               "bioguideId": item
                           }),
                           {
                               "X-Parse-Application-Id": PARSE_APP_ID,
                               "X-Parse-REST-API-Key": PARSE_REST_KEY,
                               "Content-Type": "application/json"
                           })
        result = json.loads(connection.getresponse().read())
        print "save result for saving failed bioguides:", result
    return None

def failedBeforePhantomEmails(bioguide):
    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connection.connect()
    params = urllib.urlencode({"where": json.dumps({
        "bioguideId": {"$in": bioguide}
    })})
    connection.request('GET', '/parse/classes/CongressEmailFieldsUpdateLog?%s' % params,
                       '',
                       {
                           "X-Parse-Application-Id": PARSE_APP_ID,
                           "X-Parse-REST-API-Key": PARSE_REST_KEY,
                           "Content-Type": "application/json"
                       })
    result = json.loads(connection.getresponse().read())
    print "get required fields_parse result", result['results']
    return result['results']
    return True

def get_missing_bioguides(bioguideArray,required_fields_objects):
    missing_bioguide_array = []

    for item in bioguideArray:
        found = False
        for item2 in required_fields_objects:
            if item == item2['bioguideId']:
                found = True
        if not found:
            missing_bioguide_array.append(item)
    print "missing_bioguide_array", missing_bioguide_array


    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connection.connect()
    params = urllib.urlencode({"where":json.dumps({
           "bioguideId": {"$in": missing_bioguide_array}
         })})
    connection.request('GET', '/parse/classes/CongressRequiredEmailFieldsPhantomFailList?%s' % params,
                       '',
                       {
                           "X-Parse-Application-Id": PARSE_APP_ID,
                           "X-Parse-REST-API-Key": PARSE_REST_KEY,
                           "Content-Type": "application/json"
                       })
    failedArray = json.loads(connection.getresponse().read())
    failedArray = failedArray['results']
    print failedArray
    still_missing_bioguide_array = []

    for item in missing_bioguide_array:
        found = False
        for item2 in failedArray:
            print item2
            if item == item2['bioguideId']:
                found = True
        if not found:
            still_missing_bioguide_array.append(item)
    print "still_missing_bioguide_array", still_missing_bioguide_array
    return still_missing_bioguide_array


def get_congress_required_fields_parse(bioguideArray):
    # print "bioguideArray at start of parse fetch", bioguideArray
    # print type(bioguideArray)
    # bioguideArrayJson = json.loads(bioguideArray)

    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connection.connect()
    params = urllib.urlencode({"where":json.dumps({
           "bioguideId": {"$in": bioguideArray}
         })})
    connection.request('GET', '/parse/classes/CongressRequiredEmailFields?%s' % params,
                       '',
                       {
                           "X-Parse-Application-Id": PARSE_APP_ID,
                           "X-Parse-REST-API-Key": PARSE_REST_KEY,
                           "Content-Type": "application/json"
                       })
    result = json.loads(connection.getresponse().read())
    print "get required fields_parse result", result['results']
    return result['results']


def get_congress_email_fields_phantom(bioguideArray):
    # bioguideArray = json.loads(bioguideArray)
    dataString = json.dumps({"bio_ids": bioguideArray})

    connection = httplib.HTTPSConnection('congressforms.eff.org')
    connection.connect()
    connection.request("POST", "/retrieve-form-elements/",
        dataString,
        {#headers
           "Content-Type": "application/json"
        })
    required_fields_object = json.loads(connection.getresponse().read())
    print "required fields object from phantom: :", required_fields_object
    save_result =  save_fields(required_fields_object)
    return save_result

def save_fields(required_fields_object):
    print "fields_array before save:", required_fields_object
    # required_fields = required_fields_object[bioguideId]["required_actions"]

    save_result_array = []

    for key,value in required_fields_object.items():
        print key
        bioguide_id = key
        required_fields = value['required_actions']
        print required_fields
        for field in required_fields:
            field['value'] = field['value'].replace('$','')
            if field['value'] == 'NAME_PREFIX':
                optionsDict = field['options_hash']
                print "TTTTTTTTTTTTTTTT: ", type(optionsDict)
                # typeString = str(type(optionsDict))
                # print typeString
                if isinstance(optionsDict,dict):
                    print "yes, dictionary"
                    # optionsDictNew = {}
                    print optionsDict
                    for keya, valuea in optionsDict.items():
                        print keya
                        newKey = keya.replace('.','')
                        print newKey
                        optionsDict[newKey] = optionsDict.pop(keya)
                    # field['options_hash'] = optionsDictNew
                elif isinstance(optionsDict,list):
                    print "no, list"
                    for item in optionsDict:
                        newItem = item.replace('.','')
                        item = newItem
                else:
                    print "Nothing is triggering"
                    del field
                    # field['option_hash'] = optionsListNew
                # for it in optionDict:
                #     new = it.replace('.', '')
                #     it = new
                #     print "item:", type(item)
                #     for i in item:
                #         if i == '.':
                #             print "YES YES YES"
                #             i = ''
                #         print "new item:", i
            elif field['value'] == 'TOPIC':
                optionsDict = field['options_hash']
                try:
                    for key, value in optionsDict.items():
                        newKey = key.replace('.', '').replace('   ',' ').replace('/', '').replace(',', '').replace('$','')
                        optionsDict[newKey] = optionsDict.pop(key)
                except:
                    for item in optionsDict:
                        newItem = item.replace('.', '').replace('   ', ' ').replace('/', '').replace(',', '').replace('$','')
                        item = newItem
        print "after replace::::::::::::", required_fields


         # Save the entry from phantom congress
        connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
        connection.connect()
        connection.request('POST', '/parse/classes/CongressRequiredEmailFields',
        json.dumps({
            "bioguideId": bioguide_id,
            "required_fields": required_fields
        }),
       {
           "X-Parse-Application-Id": PARSE_APP_ID,
           "X-Parse-REST-API-Key": PARSE_REST_KEY,
           "Content-Type": "application/json"
       })
        result = json.loads(connection.getresponse().read())
        print "save result for required fields::::::", result
        # save_result_array.append(result)



        # get the entry that was just saved and apppend to array
        connection2 = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
        connection2.connect()
        params = urllib.urlencode({"where": json.dumps({
            "bioguideId": bioguide_id
        })})
        connection2.request('GET', '/parse/classes/CongressRequiredEmailFields?%s' % params,
                            '',
                            {
                                "X-Parse-Application-Id": PARSE_APP_ID,
                                "X-Parse-REST-API-Key": PARSE_REST_KEY,
                                "Content-Type": "application/json"
                            })
        result2 = json.loads(connection2.getresponse().read())
        result2 = result2['results']
        print "get required fields_parse result", result2



        # append the fetched phantom congress, but now parse required fields items.
        save_result_array.append(result2)
        return save_result_array
    return save_result_array

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