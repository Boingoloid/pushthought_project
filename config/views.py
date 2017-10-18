# coding=utf-8
from __future__ import unicode_literals

import tweepy
import re
import json

from allauth.compat import reverse
from allauth.socialaccount.helpers import (
    complete_social_login,
    render_authentication_error,
)
from allauth.socialaccount.providers.oauth.client import OAuthError
from allauth.socialaccount.providers.base import AuthError
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from allauth.socialaccount.providers.oauth.views import OAuthLoginView, OAuthView
from allauth.socialaccount.models import SocialApp, SocialToken, SocialLogin
from allauth.account.views import LoginView



from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import View
from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.db.utils import IntegrityError


from actions.models import Action
from congress.models import Congress
from campaigns.models import Campaign

from . import forms

class LoginView(LoginView):
    form_class = forms.Login


login = LoginView.as_view()

class LoggedInView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            token_obj = SocialToken.objects.filter(account__user_id=request.user.id, account__provider='twitter')\
                .exists()
            if token_obj:
                text = ''
            else:
                text = "/accounts/twitter/login/?process=connect"
        else:
            text = "/accounts/twitter/login/?process=login"

        return HttpResponse(text)


class TwitterLoginView(OAuthLoginView):
    def dispatch(self, request, *args, **kwargs):
        resp = super(TwitterLoginView, self).dispatch(request, *args, **kwargs)
        tweet_text = request.POST.get('tweet_text')
        program_id = request.POST.get('program_id')

        campaign_id = request.POST.get('campaign_id')

        address_array = request.POST.get('address_array')
        bioguide_array = request.POST.get('bioguide_array')

        request.session['redirect_url'] = request.META.get('HTTP_REFERER', '/')
        request.session['tweet_text'] = tweet_text
        request.session['sent_tweet'] = False

        request.session['program_id'] = program_id
        request.session['campaign_id'] = campaign_id

        request.session['address_array'] = address_array
        request.session['bioguide_array'] = bioguide_array
        return resp


class OAuthCallbackView(OAuthView):
    def dispatch(self, request):
        """
        View to handle final steps of OAuth based authentication where the user
        gets redirected back to from the service provider
        """
        login_done_url = reverse(self.adapter.provider_id + "_callback")
        client = self._get_client(request, login_done_url)
        if not client.is_valid():
            if 'denied' in request.GET:
                error = AuthError.CANCELLED
            else:
                error = AuthError.UNKNOWN
            extra_context = dict(oauth_client=client)
            return render_authentication_error(
                request,
                self.adapter.provider_id,
                error=error,
                extra_context=extra_context)
        app = self.adapter.get_provider().get_app(request)
        try:
            access_token = client.get_access_token()
            token = SocialToken(
                app=app,
                token=access_token['oauth_token'],
                # .get() -- e.g. Evernote does not feature a secret
                token_secret=access_token.get('oauth_token_secret', ''))
            self.token = token
            login = self.adapter.complete_login(request,
                                                app,
                                                token,
                                                response=access_token)
            login.token = token
            login.state = SocialLogin.unstash_state(request)
            return complete_social_login(request, login)
        except OAuthError as e:
            return render_authentication_error(
                request,
                self.adapter.provider_id,
                exception=e)


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
        if request.user.is_authenticated and redirect_url and self.tweet_text:
            self.api = self.get_authed_twitter_api()
            self.mentions = self.get_mentions()
            self.clean_tweet_text = self.get_clean_tweet_text()
            self.send_tweets()
            request.session['alertList'] = json.dumps([self.successArray, self.duplicateArray])

            return HttpResponseRedirect(request.session.get('redirect_url'))
        elif redirect_url and not self.tweet_text:
            return HttpResponseRedirect(request.session.get('redirect_url'))
        else:
            return resp

    def get_authed_twitter_api(self):
        try:
            token_obj = SocialToken.objects.get(account__user=self.request.user, account__provider='twitter')
        except SocialToken.DoesNotExist:
            token_obj = self.token

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

                campaign = Campaign.objects.get(slug=self.campaign)
                Action.tweets.create(
                    tweet_text_with_metion,
                    user=self.request.user,
                    campaign=campaign,
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