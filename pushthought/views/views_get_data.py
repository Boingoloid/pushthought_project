import json, httplib, urllib
from views import *
from ..forms import SegmentForm
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.conf import settings
from ..models import Program


PARSE_APP_ID = settings.PARSE_APP_ID
PARSE_REST_KEY = settings.PARSE_REST_KEY

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
    # program_list = connection.getresponse().read()
    # print "return from get-programs:", program_list
    program_list_results = json.loads(connection.getresponse().read())
    program_list = program_list_results['results']
    print program_list
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
    print "Printing program list for user"
    print program_list['results']
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
def get_tweet_data(segmentId):
    segmentId = 'JPGM9mmcKV'
    # Query for tweets
    connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    params = urllib.urlencode({
        "where":json.dumps({
            "segmentObjectId":segmentId,
            "messageType": "twitter"
        }),
        "order":"-_create"
                "d_at"})
    connection.connect()
    connection.request('GET', '/parse/classes/sentMessages?%s' % params, '', {
           "X-Parse-Application-Id": PARSE_APP_ID,
           "X-Parse-REST-API-Key": PARSE_REST_KEY
         })

    tweet_data = json.loads(connection.getresponse().read())
    # print "Tweet data"
    # print tweet_data
    return tweet_data['results']

#helper
def get_petition_url(action_list):
    for item in action_list:
        if item['actionCategory'] == "Petition":
            petition_url = item['petitionURL']
    return petition_url


#helper
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

#helper
def save_tweet_action(request, tweet_text, current_user,twitter_user): #helper
    connectionTweet = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
    connectionTweet.connect()
    connectionTweet.request('POST', '/parse/classes/SentMessages', json.dumps({
        "messageText": tweet_text,
        "actionCategory": "Local Representative",
        "messageCategory": "Local Representative",
        "messageType": "twitter",
        "userObjectId": current_user['objectId'],
        "twitterUserName": twitter_user.screen_name,
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
            "actionCategory": "Local Representative",
            "messageCategory": "Local Representative",
            "messageType": "twitter",
            "userObjectId": current_user['objectId'],
            "twitterUserName": twitter_user.screen_name,
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
            "actionCategory": "Local Representative",
            "messageCategory": "Local Representative",
            "messageType": "twitter",
            "userObjectId": current_user['objectId'],
            "twitterUserName": twitter_user.screen_name,
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
            "programObjectId": request.session['programId']
        })
    })
    connection.connect()
    connection.request('GET', '/parse/classes/SegmentStats?%s' % params, '', {
       "X-Parse-Application-Id": PARSE_APP_ID,
       "X-Parse-REST-API-Key": PARSE_REST_KEY
     })
    result = json.loads(connection.getresponse().read())
    print "downloaded segment stats:", result['results']
    data = result['results']

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
               "actionCount": action_count
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