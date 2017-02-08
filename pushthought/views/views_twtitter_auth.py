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

    request.session['tweetText'] = data['tweet_text']
    request.session['programId'] = data['program_id']
    request.session['segmentId'] = data['segment_id']
    request.session['lastMenuURL'] = data['last_menu_url']
    request.session['successArray'] = data['successArray']
    request.session.modified = True

    print "program id in session:", request.session['programId']
    print "successsArray in session:", request.session['successArray']

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
        print "current User retrieved" , current_user
        try:
            if current_user['code'] == 209:
                print "yes, status is 209, invalid session token, sending ot twitter"
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
            print "no code 209"

        # Gather twitter keys
        access_key_token = current_user['authData']['twitter']['auth_token']
        access_key_token_secret = current_user['authData']['twitter']['auth_token_secret']

        twitter_user = current_user['twitter_user']
        # print "type twitter_user :" type(twitter_user)


        # print "screen_name", twitter_user.screen_name
        # save twitter profile data to current_user
        # update_user_with_twitter_profile_data(request, current_user,twitter_user,access_key_token,access_key_token_secret)

        #  Gather data to sent tweet from session
        #     tweet_text
        try:
            tweet_text = request.session['tweetText']
            del request.session['tweetText']
            request.session.modified = True
        except:
            print "hit error while finding/deleting tweetText in session"

        #  Send meesage if tweet text
        if not tweet_text:
            print "verify catch done, NO message to send"
        else:
            # send tweet
            send_tweet_with_tweepy(tweet_text, access_key_token, access_key_token_secret)

            # save tweet
            action_object_id = save_tweet_action(request, tweet_text,current_user,twitter_user)

            # Save #'s
            save_hashtags(request,tweet_text,current_user,twitter_user,action_object_id)

            # Save @'s
            save_targets(request,tweet_text,current_user,twitter_user, action_object_id)

            # Save to SegmentStats
            update_segment_stats(request)

        # redirect to last landing page if programId
        if request.session['programId']:
            redirectURL = "/content_landing/" + request.session['programId']
            print "here is the redirect url flag 1", redirectURL
            return HttpResponse(json.dumps({'redirectURL': redirectURL}), content_type="application/json")
        else:
            redirectURL = "/browse/"
            print "here is the redirect to browse", redirectURL
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
        # return HttpResponseRedirect(redirect_url)
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

    #  Gather data to sent tweet from session
    #     tweet_text
    try:
        tweet_text = request.session['tweetText']
        del request.session['tweetText']
        request.session.modified = True
    except:
        print "hit error while deleting"


    #     programId
    try:
        programId = request.session['programId']
    except:
        programId = None


    #  Send meesage if tweet text
    if not tweet_text:
        print "verify catch done, NO message to send"
    else:
        # send tweet
        send_tweet_with_tweepy(tweet_text, access_key_token, access_key_token_secret)

        # save tweet
        action_object_id = save_tweet_action(request, tweet_text,current_user,twitter_user)

        # Save #'s
        save_hashtags(request,tweet_text,current_user,twitter_user,action_object_id)

        # Save @'s
        save_targets(request,tweet_text,current_user,twitter_user, action_object_id)

        # Save to SegmentStats
        update_segment_stats(request)

    # redirect to last landing page if programId
    if programId:
        redirectURL = "/content_landing/" + programId
        print "here is the redirect url", redirectURL
        print "successArray", request.session['successArray']
        return HttpResponseRedirect(redirectURL)
    else:
        redirectURL = "/browse/"
        print "here is the redirect to brose to browse", redirectURL
        return HttpResponseRedirect(redirectURL)


#helper
def send_tweet_with_tweepy(tweet_text,access_key_token,access_key_token_secret): #helper
    CALLBACK_URL = TWITTER_CALLBACK_ROOT_URL
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, CALLBACK_URL)
    auth.set_access_token(access_key_token, access_key_token_secret)
    api = tweepy.API(auth)
    api.update_status(tweet_text)
    print "tweet sent"
    return None

        # import ast
        # d = ast.literal_eval(twitter_user)
        # print "d:", d
        # print "type d:", type(d)