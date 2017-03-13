import json, httplib, urllib
from views import *
from ..forms import SegmentForm
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.conf import settings
from ..models import Program
import requests
from bson.son import SON
import pymongo


MONGODB_URI = settings.MONGODB_URI

PARSE_APP_ID = settings.PARSE_APP_ID
PARSE_REST_KEY = settings.PARSE_REST_KEY



# API
def get_congress(request,zip):
    # Save zip to Session
    request.session['zip'] = zip
    print "zip:", zip

    # Save zip to user:
    try:
        current_user = request.session['currentUser']
    except:
        current_user = None
        print "no user logged in, passing key error on currentUser while saving zip."

    # get programId from session if available, use to pull user messages:
    try:
        segment_id = request.session['segmentId']
    except:
        segment_id = None
        print "no segmentId during get congress, so cannot pull stats or user previous messages."

    if segment_id:
        segment_congress_stats = get_congress_stats_for_program(segment_id)
        print "printing congress stats on get_congress:", segment_congress_stats

    if current_user:
        save_result = save_zip_to_user(request, zip)
        print "zip to user result:", save_result
        if segment_id:
            message_list = get_segment_actions_for_user(segment_id, current_user['objectId'])
        else:
            message_list = []
    else:
        message_list = []

    # Return congress based on location
    congress_data_raw = get_congress_data(zip)
    congress_data_raw = add_title_and_full_name(congress_data_raw)
    congress_photos = get_congress_photos(congress_data_raw)
    congress_data = add_congress_photos(congress_data_raw,congress_photos)
    congress_data = add_congress_stats(congress_data,segment_congress_stats)

    if message_list:
        congress_data = add_prior_activity_to_congress_data(congress_data, message_list)
    print "made it here, sending success response with congressData"
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
    print result
    return result




#helper
def move_to_front(list,value):
    indexNum = list.index(value)
    poppedItem = list.pop(indexNum)
    list.insert(0,poppedItem)
    return list

#helper
def get_congress_data(zip_code):

    client = pymongo.MongoClient(MONGODB_URI)
    db = client.get_default_database()

    root = "https://congress.api.sunlightfoundation.com/legislators/locate"

    #HELPER FUNCTION: nested function to get Congress Data from api, then save in CongressData under the zip_code
    def get_congress_data_from_api():
        urlAPI = root + "?zip=" + zip_code + "&apikey=" + settings.SUNLIGHT_LABS_API_KEY
        r = requests.get(urlAPI)
        results = json.loads(r.content)['results']

        def save_to_congress_data_collection():
            save_dictionary = { "zip_code": zip_code, "results": results}
            save_result = db.CongressData.insert_one(save_dictionary)
            # get image:
            # print "results of save: ", save_result.inserted_id
            return save_result

        if len(results) != 0:
            save_to_congress_data_collection()
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
        delete_result = db.CongressData.delete_many({"zip_code": zip_code})
        print "deleted CongressData documents count:", delete_result.deleted_count
        return get_congress_data_from_api()



#helper
def get_congress_photos(congress_data):
    # create bioguide array from congress data (tells who we need photos for)
    bioguide_array = []
    for item in congress_data:
        bioguide_array.append(item['bioguide_id'])

    # Query for photos
    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    params = urllib.urlencode({"where":json.dumps({
           "bioguideId": {
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

#helper
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

#helper
def add_congress_photos(congress_data,photo_data):
    for personItem in congress_data:
        for photoItem in photo_data:
            if str(personItem['bioguide_id']) == str(photoItem['bioguideId']):
                personItem['image'] = photoItem['image']
                # print personItem
                # print photoItem
    return congress_data



#helper
def add_prior_activity_to_congress_data(congress_data,message_list):
    for item in congress_data:
        try:
            twitter_id = item['twitter_id']
        except:
            twitter_id = None

        if twitter_id:
            twitter_id = item['twitter_id']
            for message in message_list:
                try:
                    target_address = message['targetAddress']
                except:
                    target_address = None
                if(target_address):
                    # print "twitter_id", twitter_id
                    # print "target_address", target_address
                    if target_address == twitter_id:
                        item['userTouched'] = 1
                        # print "YES! user touched!!! " , twitter_id
                        # print congress_data
    return congress_data

def get_congress_stats_for_program(segment_id):
    client = pymongo.MongoClient(MONGODB_URI)
    db = client.get_default_database()
    pipeline = [{"$match": {"segmentObjectId": segment_id}},
                {"$group": {"_id": "$targetBioguideId", "count": {"$sum": 1}}},
                {"$sort": SON([("count", -1), ("_id", -1)])}]
    array = []
    result = db.SentMessages.aggregate(pipeline)
    for doc in result:
        doc['targetBioguideId'] = doc['_id']
        array.append(doc)
    # print "print get_congress_stats_array result:",array
    return array


def add_congress_stats(congress_data, segment_congress_stats):
    for personItem in congress_data:
        for dataItem in segment_congress_stats:
            if str(personItem['bioguide_id']) == str(dataItem['targetBioguideId']):
                personItem['sent_messages_count'] = dataItem['count']
                # personItem['user_count'] =
    return congress_data



