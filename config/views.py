# coding=utf-8
from __future__ import unicode_literals

import tweepy

from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from allauth.socialaccount.providers.oauth.views import OAuthCallbackView, OAuthLoginView
from allauth.socialaccount.models import SocialApp, SocialToken

from django.http import HttpResponseRedirect
from django.views.generic import View
from django.http.response import HttpResponse


class LoggedInView(View):
    def get(self, request, *args, **kwargs):
        text = False
        if request.user.is_authenticated():
            text = True

        return HttpResponse(text)


class TwitterLoginView(OAuthLoginView):
    def dispatch(self, request, *args, **kwargs):
        resp = super(TwitterLoginView, self).dispatch(request, *args, **kwargs)
        tweet_text = request.POST.get('tweet_text')
        request.session['redirect_url'] = request.META['HTTP_REFERER']
        request.session['tweet_text'] = tweet_text
        request.session['sent_tweet'] = False
        return resp


class TwitterCallbackView(OAuthCallbackView):
    def dispatch(self, request, *args, **kwargs):
        resp = super(TwitterCallbackView, self).dispatch(request, *args, **kwargs)
        self.tweet_text = request.session.get('tweet_text')
        request.session['sent_tweet'] = True
        redirect_url = request.session.get('redirect_url')
        if redirect_url:
            self.send_tweet()
            return HttpResponseRedirect(request.session.get('redirect_url'))
        else:
            return resp

    def send_tweet(self):  # helper
        # CALLBACK_URL = TWITTER_CALLBACK_ROOT_URL

        token_obj = SocialToken.objects.get(account__user=self.request.user, account__provider='twitter')

        TWITTER_CONSUMER_SECRET = SocialApp.objects.filter(provider='twitter').last().secret
        TWITTER_CONSUMER_KEY = SocialApp.objects.filter(provider='twitter').last().client_id


        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_access_token(token_obj.token, token_obj.token_secret)
        api = tweepy.API(auth)

        # try:
        #     program_id = self.request.session.get('programId')
        #     urlText = 'http://www.pushthought.com/content_landing/' + program_id
        # except:
        #     print("no program Id to send MEDIA with tweet")

        tweet_text_final = self.tweet_text
        print(tweet_text_final)
        # need link to action menu
        try:
            api.update_status(tweet_text_final)
            print("tweet sent")
            return True
        except tweepy.TweepError as e:
            print(e)
            return e.api_code

oauth_login = TwitterLoginView.adapter_view(TwitterOAuthAdapter)
oauth_callback = TwitterCallbackView.adapter_view(TwitterOAuthAdapter)