import re
import time
import json
import httplib
import tweepy

from allauth.socialaccount.models import SocialApp, SocialToken

from django.views.generic import View
from django.http import JsonResponse

from actions.models import Action
from programs.models import Program
from congress.models import Congress

from views_alerts import *
from views_get_data import *
from views_user_forms import *


TWITTER_CONSUMER_SECRET = SocialApp.objects.filter(provider='twitter').last().secret
TWITTER_CONSUMER_KEY = SocialApp.objects.filter(provider='twitter').last().client_id
TWITTER_CALLBACK_ROOT_URL = 'http://127.0.0.1:8000/accounts/twitter/login/callback/'

def verify_twitter(request):
    print "verify twitter running"
    # print "send contact function!"
    # print "request.body:", request.body
    # print "request.GET:", request.GET
    # print "request.POST", request.POST
    # print "request.META", request.META

    data = json.loads(request.body)
    print "printing body of request made to verify_twitter", data

    request.session['programId'] = data['program_id']
    request.session['segmentId'] = data['segment_id']
    request.session['lastMenuURL'] = data['last_menu_url']
    request.session['addressArray'] = data['address_array']
    request.session['bioguideArray'] = data['bioguide_array']
    request.session['tweetText'] = data['tweet_text']
    tweet_text = request.session['tweetText']
    request.session.modified = True

    if request.user.is_anonymous():
        ref = request.META['HTTP_REFERER']
        return HttpResponse('/accounts/twitter/login/?process=login&next=' + ref, status=201)

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
                auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, CALLBACK_URL)
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
        overMax = False
        success = False
        duplicate = False
        other = False
        address_array = request.session['addressArray']
        bioguide_array = request.session['bioguideArray']

        if len(address_array) == 0:
            target_address = None
            target_bioguide = None
            result = send_tweet_and_save_action(request, tweet_text, access_key_token, access_key_token_secret, current_user, twitter_user, target_address, target_bioguide)

            if result == True:
                success = True
            elif result == 187:
                duplicate = True
            elif result == 186:
                overMax = True
            else:
                other = True

        elif len(address_array) == 1:
            a_array = [x.encode('UTF8') for x in address_array]
            target_address = address_array[0]
            target_bioguide = bioguide_array[0]
            result = send_tweet_and_save_action(request, tweet_text, access_key_token, access_key_token_secret,current_user, twitter_user, target_address, target_bioguide)
            if result == True:
                successArray.append(target_address)
            elif result == 187:
                duplicateArray.append(target_address)
            elif result == 186:
                overMax = True
            else:
                otherErrorArray.append(target_address)
        else:
            i = 0
            a_array = [x.encode('UTF8') for x in address_array]
            b_array = []
            for item in a_array:
                new_item = item.replace('\n','');
                b_array.append(new_item)
            print "b array", b_array
            for itemb in b_array:
                target_address = itemb
                target_bioguide = bioguide_array[i]
                print "print length of address array:", len(address_array)
                if (len(address_array) > 1):
                    tweet_replace = tweet_text.replace('@multiple', target_address)
                    result = send_tweet_and_save_action(request, tweet_replace, access_key_token, access_key_token_secret,current_user, twitter_user, target_address, target_bioguide)
                if result == True:
                    successArray.append(target_address)
                elif result == 187:
                    duplicateArray.append(target_address)
                elif result == 186:
                    overMax = True
                else:
                    otherErrorArray.append(target_address)
                i = i + 1
                time.sleep(1)  # delays for 1 seconds

        # redirect to last landing page if segmentId
        try:
            segmentId = request.session['programId']
        except:
            segmentId = None
        if segmentId:
            return HttpResponse(json.dumps({'send_response': successArray,'successArray': successArray,'duplicateArray': duplicateArray, 'otherErrorArray': otherErrorArray,'overMax':overMax,'success':success,'duplicate':duplicate,'other':other}), content_type="application/json")
        else:
            redirectURL = "/browse/"
            print "redirect to browse no segmentId", redirectURL
            return HttpResponse(json.dumps({'redirectURL': redirectURL}), content_type="application/json")
    else:
        print "SessionToken and userObjectUd NOT found, send to twitter auth"
        CALLBACK_URL = settings.TWITTER_CALLBACK_ROOT_URL
        print "callback url", CALLBACK_URL

        # App level auth
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        redirectURL = auth.get_authorization_url()

        # Store session value b/c sending to twitter for auth
        request.session['requestToken'] = auth.request_token
        request.session.modified = True

        print "redirect url down here", redirectURL
        return HttpResponse(json.dumps({'redirectURL': redirectURL}), content_type="application/json")


class SendTweetView(View):
    def post(self, request, *args, **kwargs):
        self.response = {}
        self.set_session()
        self.api = self.get_authed_twitter_api()
        self.mentions = self.get_mentions()
        if not len(self.mentions):
            return JsonResponse({'status': 'noMention'})

        self.clean_tweet_text = self.get_clean_tweet_text()
        self.send_tweets()

        return JsonResponse({
            'send_response': self.successArray,
            'successArray': self.successArray,
            'duplicateArray': self.duplicateArray
        })

    def set_session(self):
        self.successArray = []
        self.duplicateArray = []
        data = self.request.POST
        self.request.session['programId'] = data['program_id']
        self.request.session['segmentId'] = data['segment_id']
        self.request.session['lastMenuURL'] = data['last_menu_url']
        self.request.session['tweetText'] = data['tweet_text']
        self.request.session['addressArray'] = data.getlist('address_array[]')
        self.request.session['bioguideArray'] = data['bioguide_array[]']
        self.tweet_text = data['tweet_text']
        self.program = Program.objects.get(pk=data['program_id'])
        self.request.session.modified = True

    def get_authed_twitter_api(self):
        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        token_obj = SocialToken.objects.get(account__user=self.request.user, account__provider='twitter')
        auth.set_access_token(token_obj.token, token_obj.token_secret)
        api = tweepy.API(auth)
        return api

    def get_mentions(self):
        mentionlist = self.request.session['addressArray']
        mentions = [mention.replace('@', '') for mention in mentionlist]
        return mentions

    def get_clean_tweet_text(self):
        pattern = r'@\w+,?\s'
        replacement = ''
        clean_text = re.sub(pattern, replacement, self.tweet_text)
        return clean_text

    def send_tweet(self, mention):
        #TODO: create a general function
        tweet_text_with_metion = '@{} {}'.format(mention, self.clean_tweet_text)
        congress = Congress.objects.get(twitter_id=mention)

        if len(tweet_text_with_metion) > 140:
            return JsonResponse({ 'status': 'overMax'})

        try:
            self.api.update_status(tweet_text_with_metion)
            Action.tweets.create(
                tweet_text_with_metion,
                user=self.request.user,
                program=self.program,
                congress=congress
            )
            self.successArray.append('@{}'.format(mention))
            return False
        except tweepy.TweepError as e:
            print(e)
            if e.api_code == 187:
                self.duplicateArray.append('@{}'.format(mention))

            return e.api_code

    def send_tweets(self):
        for mention in self.mentions:
            self.send_tweet(mention)


def verify_catch(request):



    print "verify catch starting"
    # Establish auth connection using Ap identification
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    # Get Access Key
    token_obj = SocialToken.objects.get(account__user=request.user, account__provider='twitter')

    access_key_token = token_obj.token
    access_key_token_secret = token_obj.token_secret

    # Establish API connection
    auth.set_access_token(token_obj.token, token_obj.token_secret)

    successArray = []
    duplicateArray = []
    otherErrorArray = []
    overMax = False
    success = False
    duplicate = False
    other = False
    address_array = request.session['addressArray']
    bioguide_array = request.session['bioguideArray']
    tweet_text = request.session['tweetText']

    if (len(address_array) == 0):
        target_address = None
        target_bioguide = None
        result = send_tweet_and_save_action(request, tweet_text, access_key_token, access_key_token_secret, current_user, twitter_user, target_address, target_bioguide)
        if result == True:
            success = True
        elif result == 187:
            duplicate = True
        elif result == 186:
            overMax = True
        else:
            other = True

    elif len(address_array) == 1:
        a_array = [x.encode('UTF8') for x in address_array]
        target_address = address_array[0]
        target_bioguide = bioguide_array[0]
        result = send_tweet_and_save_action(request, tweet_text, access_key_token, access_key_token_secret,current_user, twitter_user, target_address, target_bioguide)
        if result == True:
            successArray.append(target_address)
        elif result == 187:
            duplicateArray.append(str(target_address))
        elif result == 186:
            overMax = True
        else:
            otherErrorArray.append(target_address)

    else:
        i = 0
        a_array = [x.encode('UTF8') for x in address_array]
        b_array = []
        for item in a_array:
            new_item = item.replace('\n', '')
            b_array.append(new_item)
        for itemb in b_array:
            target_address = itemb
            target_bioguide = bioguide_array[i]
            if (len(address_array) > 1):
                tweet_replace = tweet_text.replace('@multiple', target_address)
            result = send_tweet_and_save_action(request, tweet_replace, access_key_token, access_key_token_secret,current_user, twitter_user, target_address, target_bioguide)
            print "Result of send tweet attempt:", result
            if result == True:
                successArray.append(item)
            elif result == 187:
                duplicateArray.append(str(item))
            elif result == 186:
                overMax = True
            else:
                otherErrorArray.append(item)
            i = i + 1
            time.sleep(2)  # delays for 2 seconds
    try:
        segmentId = request.session['programId']
    except:
        programId = None
    if segmentId:
        alertList = [successArray, duplicateArray, otherErrorArray, overMax, success, duplicate, other]
        alertList = json.dumps(alertList)
        print "ALERT LIST:", alertList
        # print type(alertList)

        # AlertList into session
        request.session['alertList'] = alertList
        request.session.modified = True
        redirectURL = "/content_landing/" + segmentId
        print "redirecting to content_landing: ", redirectURL
        return HttpResponse(json.dumps(
            {'send_response': successArray, 'successArray': successArray, 'duplicateArray': duplicateArray,
             'otherErrorArray': otherErrorArray , 'overMax': overMax, 'success': success, 'duplicate': duplicate,
             'other': other}), content_type="application/json")
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
    print tweet_text_final
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

def send_tweet_and_save_action(request, tweet_replaced, access_key_token, access_key_token_secret, current_user,twitter_user, target_address, target_bioguide):
    # send tweet
    print "ATTEMPTING SEND WITH TWEEPY"
    result = send_tweet_with_tweepy(request, tweet_replaced, access_key_token, access_key_token_secret)
    if result == True:
        # save tweet
        action_object_id = save_tweet_action(request, tweet_replaced,current_user,twitter_user, target_address, target_bioguide)

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
    elif result == 186:
        print "over max characters (140):", result
        return result
    else:
        print "send tweet returning false, some other error"
        return result

