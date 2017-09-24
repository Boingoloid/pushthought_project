# coding=utf-8
from __future__ import unicode_literals

import tweepy
import re
import json

from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from allauth.socialaccount.providers.oauth.views import OAuthCallbackView, OAuthLoginView
from allauth.socialaccount.models import SocialApp, SocialToken

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.views.generic import View
from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.db.utils import IntegrityError


from actions.models import Action
from congress.models import Congress

from . import forms

# def StoreEmailFieldsInSessionView(request, extra_context=None):
#     query = Program.objects
#     context = dict()
#     context['programList'] = query.all().order_by('-counter')
#     context['documentaries'] = query.documentaries().order_by('-counter')
#     context['webVideoList'] = query.webvideos().order_by('-counter')
#     context['podcastList'] = query.podcasts().order_by('-counter')
#     context['otherList'] = query.other().order_by('counter')
#
#     if extra_context is not None:
#         context.update(extra_context)
#     return render(request, template, context)


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
        program_id = request.POST.get('program_id')
        campaign_id = request.POST.get('campaign_id ')
        address_array = request.POST.get('address_array')
        bioguide_array = request.POST.get('bioguide_array')

        request.session['redirect_url'] = request.META['HTTP_REFERER']
        request.session['tweet_text'] = tweet_text
        request.session['sent_tweet'] = False
        request.session['program_id '] = program_id
        request.session['campaign_id '] = campaign_id
        request.session['address_array'] = address_array
        request.session['bioguide_array'] = bioguide_array
        return resp


class TwitterCallbackView(OAuthCallbackView):
    def dispatch(self, request, *args, **kwargs):
        resp = super(TwitterCallbackView, self).dispatch(request, *args, **kwargs)
        self.successArray = []
        self.duplicateArray = []
        self.tweet_text = request.session.get('tweet_text')
        self.program = request.session.get('program_id')
        self.campaign = request.session.get('campaign_id')
        request.session['sent_tweet'] = True
        redirect_url = request.session.get('redirect_url')
        if redirect_url:
            self.api = self.get_authed_twitter_api()
            self.mentions = self.get_mentions()
            self.clean_tweet_text = self.get_clean_tweet_text()
            self.send_tweets()
            request.session['alertList'] = json.dumps([self.successArray, self.duplicateArray])

            return HttpResponseRedirect(request.session.get('redirect_url'))
        else:
            return resp

    def get_authed_twitter_api(self):
        token_obj = SocialToken.objects.get(account__user=self.request.user, account__provider='twitter')

        TWITTER_CONSUMER_SECRET = SocialApp.objects.filter(provider='twitter').last().secret
        TWITTER_CONSUMER_KEY = SocialApp.objects.filter(provider='twitter').last().client_id

        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_access_token(token_obj.token, token_obj.token_secret)
        api = tweepy.API(auth)
        return api

    def get_mentions(self):
        tweet_text = self.request.session['address_array']
        mentions = re.findall(r'@(\w+)', tweet_text)
        return mentions

    def get_clean_tweet_text(self):
        pattern = r'@\w+,?\s'
        replacement = ''
        clean_text = re.sub(pattern, replacement, self.tweet_text)
        return clean_text

    def send_tweet(self, mention):
        #TODO: create a general function
        tweet_text_with_metion = '@{} {}'.format(mention, self.clean_tweet_text)
        try:
            congress = Congress.objects.get(twitter_id=mention)
        except Congress.DoesNotExist:
            return 'Error'

        if len(tweet_text_with_metion) > 140:
            return JsonResponse({ 'status': 'overMax'})

        try:
            self.api.update_status(tweet_text_with_metion)
            if self.program:
                Action.tweets.create(
                    tweet_text_with_metion,
                    user=self.request.user,
                    program_id=self.program,
                    congress=congress
                )
            elif self.campaign:
                Action.tweets.create(
                    tweet_text_with_metion,
                    user=self.request.user,
                    campaign_id=self.campaign,
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

oauth_login = TwitterLoginView.adapter_view(TwitterOAuthAdapter)
oauth_callback = TwitterCallbackView.adapter_view(TwitterOAuthAdapter)


class SaveUserByEmailView(View):
    def post(self, request):
        form = forms.UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('email')
            raw_password = User.objects.make_random_password()
            form.instance.password = raw_password
            form.instance.username = username
            try:
                form.save()
                messages.success(request, 'Subscribed!')
            except IntegrityError:
                messages.success(request, 'Already subscribed!')
        else:
            messages.success(request, 'Invalid email!')
        return redirect('home')