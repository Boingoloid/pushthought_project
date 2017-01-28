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


    # check if user logged in.

    data = json.loads(request.body)
    print "printing body of request made to verify_twitter", data

    request.session['tweetText'] = data['tweet_text']
    request.session['programId'] = data['program_id']
    request.session['segmentId'] = data['segment_id']
    request.session['lastMenuURL'] = data['last_menu_url']
    request.session.modified = True

    try:
        sessionToken = request.session['sessionToken']
        userObjectId = request.session['userObjectId']
    except:
        sessionToken = None


    if sessionToken and userObjectId:
        print "SessionToken and userObjectUd found, validating and getting user"
        connection = httplib.HTTPSConnection('ptparse.herokuapp.com', 443)
        connection.connect()
        connection.request('GET', '/parse/classes/_User/' + userObjectId, '', {
                "X-Parse-Application-Id": PARSE_APP_ID,
                "X-Parse-REST-API-Key": PARSE_REST_KEY,
                "X-Parse-Session-Token": sessionToken
             })
        currentUser = json.loads(connection.getresponse().read())
        # print "user query returned:", currentUser
        redirectURL = "/content_landing/" + request.session['programId']
        return HttpResponse(json.dumps({'redirectURL': redirectURL}), content_type="application/json")
        # return HttpResponseRedirect('/content_landing_empty/')

        # if not result:
        #     raise ValueError
        from django.core.urlresolvers import reverse
        # idEncoded = urllib.urlencode(program_id)
        # print "id encoded: ", idEncoded
        # print "url encoded: ", url
        # url = reverse('content_landing', kwargs={'programId': program_id})
        # print "getting current_user with /me func", result2
        # return_menu = "/content_landing/" + program_id
        # # return HttpResponseRedirect(last_menu,request.session['programId'])
        # # dataDict = {}
        # # dataDict['program'] = program
        # # dataDict['programId'] = programId
        # # dataDict['congressData'] = congress_data
        # # dataDict['tweetData'] = tweet_data
        # print "return menu", return_menu
        # return HttpResponseRedirect(return_menu)
        # # return render(request, 'content_landing.html',dataDict)
        #
        # # extract data



    #     user is not logged in
    # try:
    #     print "TRYING"
    #     user_object_id = str(request.session['user_object_id'])
    #     current_user = get_parse_user_with_twitter_auth(user_object_id)
    #
    #     # Gather twitter keys -> methods below
    #     twitter_keys = { "auth_token" : current_user['authData']['twitter']['auth_token'],
    #                      "auth_token_secret" : current_user['authData']['twitter']['auth_token_secret'] }
    #     twitter_screen_name = current_user['authData']['twitter']['screen_name']
    #
    #     # Send tweet and show success
    #     send_tweet_with_tweepy(tweet_text, twitter_keys)
    #     show_tweet_success_message(request, tweet_text)
    #
    #     # Save tweet action
    #     action_object_id = save_tweet_action(request,tweet_text,current_user,twitter_screen_name)
    #
    #     # Save #'s
    #     save_hashtags(request,tweet_text,current_user,twitter_screen_name,action_object_id)
    #
    #     # Save @'s
    #     save_targets(request,tweet_text,current_user,twitter_screen_name, action_object_id)
    #
    #     # Update SegmentStats
    #     update_segment_stats(request)
    #
    #     # Post-tweet navigation
    #     if 'last_menu_url' in request.session:
    #         source_action_menu = request.session['last_menu_url']
    #         return HttpResponseRedirect(source_action_menu)
    #     else:
    #         return render(request, 'home.html')
    #
    # except:
    #     print "exception"
    else:
        print "SessionToken and userObjectUd NOT found, send to twitter auth"
        CALLBACK_URL = settings.TWITTER_CALLBACK_ROOT_URL

        # App level auth
        auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET, CALLBACK_URL)
        redirectURL = auth.get_authorization_url()

        # Store session value b/c sending to twitter for auth
        request.session['requestToken'] = auth.request_token
        request.session.modified = True

        print "redirect url", redirectURL
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

    # check if user exists
    current_user = get_user_by_twitter_screen_name(request,twitter_user.screen_name)
    if current_user:
        print "got current_user from twitter screen name", current_user
    else:
        current_user = create_user_with_twitter_auth(request, twitter_user,access_key_token,access_key_token_secret)
        print "new twitter user, created user", current_user

    # save twitter profile data to current_user
    update_user_with_twitter_profile_data(request, current_user,twitter_user,access_key_token,access_key_token_secret)



    tweet_text = request.session['tweetText']
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

    try:
        del request.session['tweetText']
        request.session.modified = True
        print "deleted tweetText"
    except:
        print "hit error while deleting"

    try:
        programId = request.session['programId']
    except:
        programId = None

    # redirect to last landing page
    if programId:
        redirectURL = "/content_landing/" + programId
        print "here is the redirect url", redirectURL
        # return HttpResponse(json.dumps({'redirect_url': redirect_url}), content_type="application/json")
        return HttpResponseRedirect(redirectURL)
    else:
        redirectURL = "/content_landing/" + programId
        print "here is the redirect url", redirectURL
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

