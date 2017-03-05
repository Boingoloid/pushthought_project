import json, httplib, urllib
from views import *
from ..forms import SegmentForm
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.conf import settings
from ..models import Program
from bson.son import SON
import pymongo


PARSE_APP_ID = settings.PARSE_APP_ID
PARSE_REST_KEY = settings.PARSE_REST_KEY
MONGODB_URI = settings.MONGODB_URI

#helper
def fetch_program_data(program_id):

    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connection.connect()
    connection.request('GET','/parse/classes/Programs/'+ program_id, '', {
        "X-Parse-Application-Id": PARSE_APP_ID,
        "X-Parse-REST-API-Key": PARSE_REST_KEY
    })
    program_dict = json.loads(connection.getresponse().read())
    return program_dict

#helper
def fetch_segment_data(segment_id):
    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connection.connect()
    connection.request('GET','/parse/classes/Segments/'+ segment_id, '', {
        "X-Parse-Application-Id": PARSE_APP_ID,
        "X-Parse-REST-API-Key": PARSE_REST_KEY
    })
    segment_dict = json.loads(connection.getresponse().read())
    return segment_dict

#helper
def get_program_list():
    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connection.connect()
    connection.request('GET','/parse/classes/Programs', '', {
        "X-Parse-Application-Id": PARSE_APP_ID,
        "X-Parse-REST-API-Key": PARSE_REST_KEY
    })
    program_list_results = json.loads(connection.getresponse().read())
    program_list = program_list_results['results']
    return program_list

    # client = pymongo.MongoClient(MONGODB_URI)
    # db = client.get_default_database()
    # program = db.Programs.find_one({"_id":programId})








def get_program_browse_stats():
    client = pymongo.MongoClient(MONGODB_URI)
    db = client.get_default_database()
    pipeline = [{"$group": {"_id": "$programObjectId", "count": {"$sum": 1}}},
                {"$sort": SON([("count", -1), ("_id", -1)])}]
    array = []
    # userArray = []


    result = db.SentMessages.aggregate(pipeline)
    for doc in result:
        doc['programObjectId'] = doc['_id']
        # print doc
        array.append(doc)
        # userArray.append(doc['userObjectId'])

    # userSet = set(userArray)
    # print "counts:", len(userArray) , " and unique: ", len(userSet)
    # for user in sorted(userArray):
    #     if user == previousUser:z
    return array

def get_program_browse_stats_user_count():

    client = pymongo.MongoClient(MONGODB_URI)
    db = client.get_default_database()

    pipeline = [{"$group": {"segmentObjectId": "$programObjectId", "count": {"$sum": 1}}},
                {"$sort": SON([("count", -1), ("segmentObjectid", -1)])}]


    pipeline = [{"$group": {
        "_id": {
            "segmentObjectId": "$segmentObjectId",
            "userObjectId": "$userObjectId"
        },
        "count": {"$sum": 1}
    }},
    {"$group": {
        "_id": {
            "segmentObjectId": "$_id.segmentObjectId",
            "userObjectId": "$_id.userObjectId"
        },
        "totalCount": {"$sum": "$count"},
        "distinctCount": {"$sum": 1}
    }}]


    result = db.SentMessages.aggregate(pipeline)
    l = []
    for doc in result:
        l.append(doc)
    l.sort(key=lambda x: (x['_id']['segmentObjectId'], x['_id']['userObjectId']))
    groupedList = simplify(l)

    print "GROUPED LIST:::::::", groupedList
    return groupedList

def combine_programs_with_stats(program_list,stats_list):
    for program_item in program_list:
        program_id = program_item['objectId']
        for stats_item in stats_list:
            stats_program_id = stats_item['segmentObjectId']
            if program_id == stats_program_id:
                program_item['sentMessagesCount'] = stats_item['totalMessages']
                program_item['userCount'] = stats_item['totalUsers']
                break
    return program_list

def simplify(list):
    previousId = ""
    currentId = ""
    totalDistinct = 0
    totalMessages = 0
    groupedList = []
    saveDict = {}

    for item in list:
        currentId = item['_id']['segmentObjectId']
        print "currentId", currentId

        if previousId == "":
            totalDistinct = item['distinctCount'] + totalDistinct
            totalMessages = item['totalCount'] + totalMessages
            print "totalMessages:", totalMessages
            previousId = currentId

        elif currentId == previousId:
            # update the total distinct number
            totalDistinct = totalDistinct + item['distinctCount']
            totalMessages = totalMessages + item['totalCount']

        else:
            saveDict['segmentObjectId'] = previousId
            saveDict['totalUsers'] = totalDistinct
            saveDict['totalMessages'] = totalMessages
            groupedList.append(saveDict)

            # Reset
            totalDistinct = item['distinctCount']
            totalMessages = item['totalCount']
            previousId = currentId
            saveDict = {}

    return groupedList



def get_program_list_with_user_stats(program_list,user_stats):
    # print "PROGRAM LIST", program_list[0]
    # print "PROGRAM STATS", program_stats

    for program_item in program_list:
        program_id = program_item['objectId']
        for stats_item in user_stats:
            stats_program_id = stats_item['_id']['segmentObjectId']
            if program_id == stats_program_id:
                program_item['userMessagesCount'] = stats_item['count']
                break
                #({'_id': program_item['programObjectId']}, {'$set': {'sentMessagesCount': program_item['count']}})
    # print "program list with stats:", program_list[0]
    return program_list







def get_program_list_with_stats(program_list,program_stats):
    # print "PROGRAM LIST", program_list[0]
    # print "PROGRAM STATS", program_stats

    for program_item in program_list:
        program_id = program_item['objectId']
        for stats_item in program_stats:
            stats_id = stats_item['programObjectId']
            # print "program_id:", program_id
            # print "stats_id:", stats_id
            if program_id == stats_id:
                program_item['sentMessagesCount'] = stats_item['count']
                break
                #({'_id': program_item['programObjectId']}, {'$set': {'sentMessagesCount': program_item['count']}})
    # print "program list with stats:", program_list[0]
    return program_list

def get_program_list_for_user(user_pk):
    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    params = urllib.urlencode({"where":json.dumps({
           "userObjectId": user_pk
         })})
    connection.connect()
    connection.request('GET','/parse/classes/Programs?%s' % params, '', {
        "X-Parse-Application-Id": PARSE_APP_ID,
        "X-Parse-REST-API-Key": PARSE_REST_KEY
    })

    program_list = json.loads(connection.getresponse().read())
    # print "Printing program list for user"
    # print program_list['results']
    return program_list['results']

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


#helper
def get_hashtag_data(segmentId):
    client = pymongo.MongoClient(MONGODB_URI)
    db = client.get_default_database()
    pipeline = [{"$match":{"segmentObjectId": segmentId}},
                {"$group": {"_id": "$hashtag", "count": {"$sum": 1}}},
                {"$sort": SON([("count", -1), ("_id", -1)])}]
    array = []
    result = db.Hashtags.aggregate(pipeline)
    for doc in result:
        doc['hashtag'] = doc['_id']
        # print doc
        array.append(doc)
    # Query for hashtags
    # connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    # params = urllib.urlencode({"where":json.dumps({
    #        "segmentObjectId":segmentId
    #      })})
    # connection.connect()
    # connection.request('GET', '/parse/classes/Hashtags?%s' % params, '', {
    #        "X-Parse-Application-Id": PARSE_APP_ID,
    #        "X-Parse-REST-API-Key": PARSE_REST_KEY
    #      })
    #
    # hashtag_data = json.loads(connection.getresponse().read())
    # print "Hashtag data"
    # print hashtag_data
    # return hashtag_data['results']
    return array




#helper
def get_tweet_data(segmentId):
    # Query for tweets
    client = pymongo.MongoClient(MONGODB_URI)
    db = client.get_default_database()
    pipeline = [{"$match":{"segmentObjectId": segmentId}},
                {"$sort": SON([("_created_at", -1)])}]
    array = []
    result = db.SentMessages.aggregate(pipeline)
    for doc in result:
        doc['sent_message'] = doc['_id']
        # print doc
        array.append(doc)
    return array

    # connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    # params = urllib.urlencode({
    #     "where":json.dumps({
    #         "segmentObjectId":segmentId,
    #         "messageType": "twitter"
    #     }),
    #     "order":"-_create"
    #             "d_at"})
    # connection.connect()
    # connection.request('GET', '/parse/classes/sentMessages?%s' % params, '', {
    #        "X-Parse-Application-Id": PARSE_APP_ID,
    #        "X-Parse-REST-API-Key": PARSE_REST_KEY
    #      })
    #
    # tweet_data = json.loads(connection.getresponse().read())
    # # print "Tweet data"
    # # print tweet_data
    # return tweet_data['results']

#helper
def get_petition_url(action_list):
    for item in action_list:
        if item['actionCategory'] == "Petition":
            petition_url = item['petitionURL']
    return petition_url


    client = pymongo.MongoClient(MONGODB_URI)
    db = client.get_default_database()
    saveReturn = db.contact_form.save(contact_data)



#helper
def save_tweet_action(request, tweet_text, current_user,twitter_user,target_bioguide): #helper
    connectionTweet = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connectionTweet.connect()
    connectionTweet.request('POST', '/parse/classes/SentMessages', json.dumps({
        "messageText": tweet_text,
        "actionCategory": "Federal Representative",
        "messageCategory": "Federal Representative",
        "messageType": "twitter",
        "userObjectId": current_user['objectId'],
        "twitterUserName": str(current_user['twitterScreenName']),
        "programObjectId" : request.session['programId'],
        "segmentObjectId" : request.session['segmentId'],
        "targetBioguideId":target_bioguide
        }), {
        "X-Parse-Application-Id": PARSE_APP_ID,
        "X-Parse-REST-API-Key": PARSE_REST_KEY,
        "Content-Type": "application/json"
    })
    result = json.loads(connectionTweet.getresponse().read())
    print "save tweet action result:", result
    action_object_id = result['objectId']
    return action_object_id

#helper
def save_hashtags(request,tweet_text,current_user,twitter_user,action_object_id):
    hashtag_list = set([i[1:] for i in tweet_text.split() if i.startswith("#")])

    for hashtag in hashtag_list:
        #search result for it
                #found exit and add one
                #move on to next
        connectionTweet = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
        connectionTweet.connect()
        connectionTweet.request('POST', '/parse/classes/Hashtags', json.dumps({
            "hashtag" : hashtag,
            "frequency" : 1,
            "messageText": tweet_text,
            "actionCategory": "Federal Representative",
            "messageCategory": "Federal Representative",
            "messageType": "twitter",
            "userObjectId": current_user['objectId'],
            "twitterUserName": str(current_user['twitterScreenName']),
            "programObjectId" : request.session['programId'],
            "segmentObjectId" : request.session['segmentId'],
            'actionObjectId' : action_object_id
            }), {
            "X-Parse-Application-Id": PARSE_APP_ID,
            "X-Parse-REST-API-Key": PARSE_REST_KEY,
            "Content-Type": "application/json"
        })
        result = json.loads(connectionTweet.getresponse().read())
        print "# save result", result
    return None

#helper
def save_targets(request,tweet_text,current_user,twitter_user,action_object_id):
    target_list = set([i[1:] for i in tweet_text.split() if i.startswith("@")])

    for target in target_list:

        connectionTweet = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
        connectionTweet.connect()
        connectionTweet.request('POST', '/parse/classes/TargetTwitterNames', json.dumps({
            "targetTwitterName" : target,
            "frequency" : 1,
            "messageText": tweet_text,
            "actionCategory": "Federal Representative",
            "messageCategory": "Federal Representative",
            "messageType": "twitter",
            "userObjectId": current_user['objectId'],
            "twitterUserName": str(current_user['twitterScreenName']),
            "programObjectId" : request.session['programId'],
            "segmentObjectId" : request.session['segmentId'],
            'actionObjectId' : action_object_id
            }), {
            "X-Parse-Application-Id": PARSE_APP_ID,
            "X-Parse-REST-API-Key": PARSE_REST_KEY,
            "Content-Type": "application/json"
        })
        result = json.loads(connectionTweet.getresponse().read())
        print "@ save result", result
    return None

#helper
def update_segment_stats(request):

    # GET current value for segment activity
    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    params = urllib.urlencode({
        "where":json.dumps({
            "segmentObjectId": request.session['programId']
        })
    })
    connection.connect()
    connection.request('GET', '/parse/classes/SegmentStats?%s' % params, '', {
       "X-Parse-Application-Id": PARSE_APP_ID,
       "X-Parse-REST-API-Key": PARSE_REST_KEY
     })
    result = json.loads(connection.getresponse().read())
    print "downloaded segment stats:", result['results']

    try:
        data = result['results'][0]
    except:
        data = None

    if data:
        action_count = data['actionCount']
        action_count = action_count + 1
        #UPDATE current value for segment activity
        connection2 = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
        connection2.connect()
        connection2.request('PUT', '/parse/classes/SegmentStats/' + data['objectId'] , json.dumps({
               "actionCount": action_count
             }), {
               "X-Parse-Application-Id": PARSE_APP_ID,
               "X-Parse-REST-API-Key": PARSE_REST_KEY,
               "Content-Type": "application/json"
             })

        result2 = connection2.getresponse().read()
        print "uploaded segment stats:", result2
    else:
        action_count = 1
        #UPDATE current value for segment activity
        connection2 = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
        connection2.connect()
        connection2.request('POST', '/parse/classes/SegmentStats', json.dumps({
                "actionCount": action_count,
                "segmentObjectId": request.session['segmentId'],
                "programObjectId": request.session['programId']
             }), {
               "X-Parse-Application-Id": PARSE_APP_ID,
               "X-Parse-REST-API-Key": PARSE_REST_KEY,
               "Content-Type": "application/json"
             })

        result2 = connection2.getresponse().read()
        print "uploaded segment stats:", result2
    return None


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

#helper
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

#helper
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