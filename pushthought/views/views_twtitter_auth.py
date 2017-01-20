from django.conf import settings
import json,httplib, urllib
from django.http import HttpResponseRedirect
import tweepy
from views_alerts import *
from views_get_data import *
from views_user_forms import *

def verify_twitter(request):
    print "ajax hitting verify twitter!"
    print "send contact function!"
    print "request.body:", request.body
    print "request.GET:", request.GET
    print "request.POST", request.POST
    print "request.session", request.session
    print "request.META", request.META

    verification_post = json.loads(request.body)
    verification_data = verification_post['data']
    tweet_text = verification_data['tweet_text']

    request.session['user_object_id'] = ''

    # check if user logged in.

    try:
        print "user has token, user id:" + request.session['user_object_id']
    except:
        print "no user object in session"

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
    print redirect_url

    # res = requests.get(redirect_url)

    # Store session value b/c sending to twitter for auth
    request.session['request_token'] = auth.request_token
    # request.session['tweetText'] = tweet_text
    # request.session['programId'] = programId
    # request.session['segmentId'] = segmentId
    request.session.modified = True
    return HttpResponseRedirect(redirect_url)

def verify_catch(request):

    print "verify catch starting"

    # Establish auth connection using Ap identification
    auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)

    # Get Request Token, then delete from session
    token = request.session['request_token']
    print "request token being used" + str(token)
    auth.request_token = token
    try:
        del request.session['request_token']
        print "deleting request token"
    except request.exceptions.HTTPError as e:
        print "And you get an HTTPError:", e.message

    # Get Access Key
    verifier = request.GET.get('oauth_verifier')
    accessKey = auth.get_access_token(verifier)
    accessKeyToken = accessKey[0]
    accessKeyTokenSecret = accessKey[1]

    # Establish API connection
    api = tweepy.API(auth)

    # Get Twitter User info
    twitter_user = api.me()
    twitter_screen_name = twitter_user.screen_name


    current_user = log_user_into_parse(twitter_user,accessKeyToken,accessKeyTokenSecret)
    print "current user:", current_user
    update_user_with_twitter_data (current_user,twitter_user,accessKeyToken,accessKeyTokenSecret)

    request.session['user_object_id'] = str(current_user['objectId'])


    # Send tweet (if available)
    if 'tweetText' in request.session:
        tweet_text = request.session['tweetText']
        del request.session['tweetText']
        api.update_status(tweet_text)
        show_tweet_success_message(request, tweet_text)
        print "tweet sent"

        # Save tweet action
        action_object_id = save_tweet_action(request,tweet_text,current_user,twitter_screen_name)

        # Save #'s
        save_hashtags(request,tweet_text,current_user,twitter_screen_name,action_object_id)

        # Save @'s
        save_targets(request,tweet_text,current_user,twitter_screen_name, action_object_id)

        # Save to SegmentStats
        update_segment_stats(request)





        request.session.modified = True

    else:
        print "verify catch NO message to send"

    # Navigation
    if 'last_menu_url' in request.session:
        source_url = request.session['last_menu_url']

        return HttpResponseRedirect(source_url)
        # return render(request, 'fed_rep_action_menu.html', {'programId'z: program, 'segmentId': segment})
    else:
        return render(request, 'home.html')


    #helper
def send_tweet_with_tweepy(tweet_text,twitter_keys): #helper
    auth_token = twitter_keys['auth_token']
    auth_token_secret = twitter_keys['auth_token_secret']
    CALLBACK_URL = TWITTER_CALLBACK_ROOT_URL
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, CALLBACK_URL)
    auth.set_access_token(auth_token, auth_token_secret)
    api = tweepy.API(auth)
    api.update_status(tweet_text)
    print "tweet sent"
    return None

