from django.conf import settings
import json,httplib, urllib
from django.http import HttpResponseRedirect
import tweepy
from views_alerts import *
from views_get_data import *
from views_user_forms import *

def verify_twitter(request):
    # print "ajax hitting verify twitter!"
    # print "send contact function!"
    # print "request.body:", request.body
    # print "request.GET:", request.GET
    # print "request.POST", request.POST
    # print "request.session", request.session
    # print "request.META", request.META




    # is user logged? yes, and looged with twitter, send?



    # check if user logged in.

    # try:
    #     print "user has token, user id:" + request.session['user_object_id']
    # #     use is logged in
    # except:
    #     print "no user object in session"
    # #     user is not logged in

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

    CALLBACK_URL = settings.TWITTER_CALLBACK_ROOT_URL

    # App level auth
    auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET, CALLBACK_URL)
    redirect_url = auth.get_authorization_url()

    # extract data
    body = json.loads(request.body)
    data = body['data']

    # Store session value b/c sending to twitter for auth
    request.session['requestToken'] = auth.request_token
    request.session['tweetText'] = data['tweet_text']
    request.session['programId'] = data['program_id']
    request.session['segmentId'] = data['segment_id']
    request.session['lastMenuURL'] = data['last_menu_url']
    request.session.modified = True

    print "redirect url", redirect_url

    return HttpResponse(json.dumps({'redirect_url': redirect_url}), content_type="application/json")

def verify_catch(request):

    print "verify catch starting"

    # Establish auth connection using Ap identification
    auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)

    # Get Request Token, then delete from session
    token = request.session['requestToken']
    print "request token being used" + str(token)
    auth.request_token = token
    del request.session['requestToken']
    print "deleting request token"

    # Get Access Key
    verifier = request.GET.get('oauth_verifier')
    accessKey = auth.get_access_token(verifier)
    access_key_token = accessKey[0]
    access_key_token_secret = accessKey[1]

    # Establish API connection
    api = tweepy.API(auth)

    # Get Twitter User info
    twitter_user = api.me()

    # print twitter_user.__dict__
    data = twitter_user.__dict__
    print data['screen_name']
    dataDump = str(data)
    print dataDump

    # check if user exists
    current_user = get_user_by_twitter_screen_name(twitter_user.screen_name)
    if current_user:
        print "user exists already for that twitter screen name, loading current_user"
    else:
        print "new twitter user, creating user"
        current_user = create_user_with_twitter_auth(twitter_user,access_key_token,access_key_token_secret)

    # save twitter profile data to current_user
    update_user_with_twitter_profile_data(current_user,twitter_user,access_key_token,access_key_token_secret)

    # save sessionToken to session
    request.session['sessionToken'] = current_user['sessionToken']
    request.session.modified = True

    tweet_text = request.session['tweetText']
    if not tweet_text:
        print "verify catch done, NO message to send"
    else:
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
        del request.session['programId']
        del request.session['segmentId']
        request.session.modified = True
        print "deleted tweetText"
    except:
        print "hit error while deleting"

    # redirect to last landing page
    if 'lastMenuURL' in request.session:
        origin_url = request.session['last_menu_url']
        del request.session['last_menu_url']
        request.session.modified = True
        return HttpResponseRedirect(origin_url)
    else:
        return render(request, 'home.html')


#helper
def send_tweet_with_tweepy(tweet_text,access_key_token,access_key_token_secret): #helper
    CALLBACK_URL = TWITTER_CALLBACK_ROOT_URL
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, CALLBACK_URL)
    auth.set_access_token(access_key_token, access_key_token_secret)
    api = tweepy.API(auth)
    api.update_status(tweet_text)
    print "tweet sent"
    return None

