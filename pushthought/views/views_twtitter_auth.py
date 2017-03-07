from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
import tweepy
from views_alerts import *
from views_get_data import *
from views_user_forms import *
import json,httplib



def verify_twitter(request):
    print "verify twitter running"
    # print "ajax hitting verify twitter!"
    # print "send contact function!"
    # print "request.body:", request.body
    # print "request.GET:", request.GET
    # print "request.POST", request.POST
    # print "request.session", request.session
    # print "request.META", request.META

    data = json.loads(request.body)
    print "printing body of request made to verify_twitter", data

    request.session['programId'] = data['program_id']
    request.session['segmentId'] = data['segment_id']
    request.session['lastMenuURL'] = data['last_menu_url']
    request.session['addressArray'] = data['address_array']
    request.session['tweetText'] = data['tweet_text']
    tweet_text = request.session['tweetText']
    request.session.modified = True

    print "program id in session:", request.session['programId']
    print "addressArray in session:", request.session['addressArray']

    try:
        sessionToken = request.session['sessionToken']
        userObjectId = request.session['userObjectId']
        print "SessionToken and userObjectUd found, validating and getting user"
    except:
        sessionToken = None

    if sessionToken and userObjectId:
        connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
        connection.connect()
        connection.request('GET', '/parse/classes/_User/' + userObjectId, '', {
                "X-Parse-Application-Id": PARSE_APP_ID,
                "X-Parse-REST-API-Key": PARSE_REST_KEY,
                "X-Parse-Session-Token": sessionToken
             })
        current_user = json.loads(connection.getresponse().read())
        # print "current User retrieved" , current_user
        try:
            if current_user['code'] == 209:
                print "yes, status is 209, invalid session token, sending to twitter."
                CALLBACK_URL = settings.TWITTER_CALLBACK_ROOT_URL

                # App level auth
                auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET, CALLBACK_URL)
                redirectURL = auth.get_authorization_url()

                # Store session value b/c sending to twitter for auth
                request.session['requestToken'] = auth.request_token
                request.session.modified = True

                print "redirect url", redirectURL
                return HttpResponse(json.dumps({'redirectURL': redirectURL}), content_type="application/json")
        except:
            print "session token ok, no code 209"

        # Gather twitter keys
        access_key_token = current_user['authData']['twitter']['auth_token']
        access_key_token_secret = current_user['authData']['twitter']['auth_token_secret']

        twitter_user = current_user['twitter_user']
        # print "addressArray length", len(request.session['addressArray'])

        successArray = []
        duplicateArray = []
        otherErrorArray = []
        address_array = request.session['addressArray']

        if (len(address_array) == 0):
            target_address = ' '
            result = send_tweet_and_save_action(request, tweet_text, access_key_token, access_key_token_secret,
                                                current_user, twitter_user, target_address)
        else:
            for item in address_array:
                target_address = str(item)
                print "print length of address array:", len(address_array)
                if (len(address_array) > 1):
                    tweet_text = tweet_text.replace('@multiple', target_address)
                result = send_tweet_and_save_action(request, tweet_text, access_key_token, access_key_token_secret,current_user, twitter_user, target_address)
                print "Result of send tweet attempt:", result
                if result == True:
                    successArray.append(item)
                elif result == 187:
                    duplicateArray.append(item)
                else:
                    otherErrorArray.append(item)

        # redirect to last landing page if programId
        try:
            programId = request.session['programId']
        except:
            programId = None
        if programId:
            return HttpResponse(json.dumps({'send_response': successArray,'successArray': successArray,'duplicateArray': duplicateArray, 'otherErrorArray': otherErrorArray}), content_type="application/json")
        else:
            redirectURL = "/browse/"
            print "redirect to browse no programId", redirectURL
            return HttpResponse(json.dumps({'redirectURL': redirectURL}), content_type="application/json")
    else:
        print "SessionToken and userObjectUd NOT found, send to twitter auth"
        CALLBACK_URL = settings.TWITTER_CALLBACK_ROOT_URL
        print "callback url", CALLBACK_URL

        # App level auth
        auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET, CALLBACK_URL)
        redirectURL = auth.get_authorization_url()

        # Store session value b/c sending to twitter for auth
        request.session['requestToken'] = auth.request_token
        request.session.modified = True

        print "redirect url down here", redirectURL
        return HttpResponse(json.dumps({'redirectURL': redirectURL}), content_type="application/json")

def verify_catch(request):
    print "verify catch starting"
    # Establish auth connection using Ap identification
    auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)

    # Get Request Token, then delete from session
    token = request.session['requestToken']
    # print "request token being used" + str(token)
    auth.request_token = token
    del request.session['requestToken']
    # print "deleting request token"

    # Get Access Key
    verifier = request.GET.get('oauth_verifier')
    accessKey = auth.get_access_token(verifier)
    access_key_token = accessKey[0]
    access_key_token_secret = accessKey[1]

    # Establish API connection
    api = tweepy.API(auth)

    # Get Twitter User info
    twitter_user = api.me()

    # check if user exists, if not create
    current_user = get_user_by_twitter_screen_name(request,twitter_user.screen_name)
    if current_user:
        print "got current_user from twitter screen name", current_user
    else:
        current_user = create_user_with_twitter_auth(request, twitter_user,access_key_token,access_key_token_secret)
        print "new twitter user, created user"

    # save twitter profile data to current_user
    update_user_with_twitter_profile_data(request, current_user,twitter_user,access_key_token,access_key_token_secret)

    #  count success array items
    #  if 0 or 1 send once with no modification
    #  if 2 or more, then execute loop, replace tweetText @multiple every time with value.  Never change tweettext base

    print "addressArray length", len(request.session['addressArray'])

    successArray = []
    duplicateArray = []
    otherErrorArray = []
    address_array = request.session['addressArray']
    tweet_text = request.session['tweetText']

    if (len(address_array) == 0):
        target_address = ' '
        result = send_tweet_and_save_action(request, tweet_text, access_key_token, access_key_token_secret,
                                            current_user, twitter_user, target_address)
    else:
        for item in address_array:
            target_address = str(item)
            if (len(address_array) > 1):
                tweet_text = tweet_text.replace('@multiple', target_address)
            result = send_tweet_and_save_action(request, tweet_text, access_key_token, access_key_token_secret,current_user, twitter_user, target_address)
            print "Result of send tweet attempt:", result
            if result == True:
                successArray.append(item)
            elif result == 187:
                duplicateArray.append(str(item))
            else:
                otherErrorArray.append(item)


    try:
        programId = request.session['programId']
    except:
        programId = None
    if programId:
        alertList = [successArray, duplicateArray, otherErrorArray]
        alertList = json.dumps(alertList)
        print "ALERT LIST:", alertList
        print type(alertList)
        request.session['alertList'] = alertList
        request.session.modified = True
        redirectURL = "/content_landing/" + programId
        print "redirecting to content_landing: ", redirectURL
        return HttpResponseRedirect(redirectURL)
    else:
        redirectURL = "/browse/"
        print "no programId redirecting to Browse:", redirectURL
        return HttpResponseRedirect(redirectURL)







from PIL import Image, ImageFilter

#helper
def send_tweet_with_tweepy(request, tweet_text,access_key_token,access_key_token_secret): #helper
    CALLBACK_URL = TWITTER_CALLBACK_ROOT_URL
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, CALLBACK_URL)
    auth.set_access_token(access_key_token, access_key_token_secret)
    api = tweepy.API(auth)

    try:
        program_id = request.session['programId']
        urlText = 'http://www.pushthought.com/content_landing/' + program_id
    except:
        print "no program Id to send MEDIA with tweet"

    tweet_text_final = tweet_text + ' ' + urlText
     # need link to action menu
    try:
        api.update_status(tweet_text_final)
        print "tweet sent"
        return True
    except tweepy.TweepError as e:
        print e
        return e.api_code

    # try:
    #     URL='http://www.pushthought.com/content_landing/'
    #     image_file = urllib.urlretrieve(URL, "000001.jpg")
    #     img = Image.open("000001.jpg")
    #
    #     filea = urllib.urlretrieve('http://www.pushthought.com/content_landing/')
    #     api.update_with_media(img, status=tweet_text)
    #     print "tweet sent with media"
    #     return True
    # except tweepy.TweepError as e:
    #     print "tweet send error:", e
    #     return e.api_code

# photo = open('/path/to/file/image.jpg', 'rb')
# response = twitter.upload_media(media=photo)
# twitter.update_status(status='Checkout this cool image!', media_ids=[response['media_id']])

def send_tweet_and_save_action(request, tweet_replaced, access_key_token, access_key_token_secret, current_user,twitter_user, target_address):
    # send tweet
    print "ATTEMPTING SEND WITH TWEEPY"
    result = send_tweet_with_tweepy(request, tweet_replaced, access_key_token, access_key_token_secret)
    if result == True:
        # save tweet
        action_object_id = save_tweet_action(request, tweet_replaced,current_user,twitter_user, target_address,)

        # Save #'s
        save_hashtags(request,tweet_replaced,current_user,twitter_user,action_object_id)

        # Save @'s
        save_targets(request,tweet_replaced,current_user,twitter_user, action_object_id)

        # Save to SegmentStats
        update_segment_stats(request)
        return True
    elif result == 187:
        print "duplicate:", result
        return result
    else:
        print "send tweet returning false, some other error"
        return result

