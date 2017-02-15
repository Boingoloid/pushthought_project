import json, httplib, urllib
from views import *
from ..forms import SegmentForm
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.conf import settings
from ..models import Program
import requests
import pymongo


MONGODB_URI = settings.MONGODB_URI

PARSE_APP_ID = settings.PARSE_APP_ID
PARSE_REST_KEY = settings.PARSE_REST_KEY

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
            print "results of save: ", save_result.inserted_id
            return save_result

        save_to_congress_data_collection()
        return results

    #MAIN: Checks UPDATE TRIGGER, then uses method above to get data locally or form api
    if not settings.CONGRESS_DATA_UPDATE_TRIGGER:
        congress_data = db.CongressData.find_one({"zip_code":zip_code})
        if congress_data:
            print "congress data returned local, no api used"
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
                personItem['imageFileURL'] = photoItem['image']
                print personItem
                print photoItem
    return congress_data