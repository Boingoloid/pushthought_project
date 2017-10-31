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
from utils.mixins import TwitterSendMixin

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

        address_array = request.POST.getlist('address_array')
        bioguide_array = request.POST.getlist('bioguide_array')

        request.session['redirect_url'] = request.META.get('HTTP_REFERER', '/')
        request.session['tweet_text'] = tweet_text
        request.session['sent_tweet'] = False

        request.session['program_id'] = program_id
        request.session['campaign_id'] = campaign_id

        request.session['addressArray'] = address_array
        request.session['bioguiderray'] = bioguide_array
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


class TwitterCallbackView(TwitterSendMixin, OAuthCallbackView):
    """
    Callback view for twitter login. Sends tweet after the user logs in.
    """
    def dispatch(self, request, *args, **kwargs):
        resp = super(TwitterCallbackView, self).dispatch(request, *args, **kwargs)

        if not request.user.is_authenticated():
            messages.error(request, 'Your twitter email address is already taken. Please login into your old account.')
            return HttpResponseRedirect('/accounts/login/')

        self.successArray = []
        self.duplicateArray = []
        self.errorArray = []
        self.tweet_text = request.session.get('tweet_text')
        self.program = request.session.get('program_id')
        self.campaign = request.session.get('campaign_id')
        request.session['sent_tweet'] = True
        redirect_url = request.session.get('redirect_url')
        if not request.user.is_authenticated:
            return resp
        if redirect_url and self.tweet_text:
            self.api = self.get_authed_twitter_api()
            if not self.api:
                return HttpResponseRedirect(request.session.get('redirect_url'))
            self.mentions = self.get_mentions()
            if not self.mentions:
                request.session['alertList'] = json.dumps({'status': 'noMention'})
            self.clean_tweet_text = self.get_clean_tweet_text()
            self.send_tweets()
            request.session['alertList'] = json.dumps([self.successArray, self.duplicateArray, self.errorArray])

            return HttpResponseRedirect(request.session.get('redirect_url'))
        elif redirect_url and not self.tweet_text:
            return HttpResponseRedirect(request.session.get('redirect_url'))
        else:
            return resp

oauth_login = TwitterLoginView.adapter_view(TwitterOAuthAdapter)
oauth_callback = TwitterCallbackView.adapter_view(TwitterOAuthAdapter)


class SaveUserByEmailView(View):
    def post(self, request):
        form = forms.UserForm(request.POST)
        if form.is_valid():
            email_exist = User.objects.filter(email=form.cleaned_data.get('email')).exists()
            if email_exist:
                messages.success(request, 'Already subscribed!')
                return redirect('home')
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
