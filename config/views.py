# coding=utf-8
from __future__ import unicode_literals

import json

from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from allauth.socialaccount.providers.oauth.views import (
    OAuthLoginView,
    OAuthCallbackView,
)
from allauth.socialaccount.models import SocialToken
from allauth.account.views import LoginView

from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import View
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.db.utils import IntegrityError

from utils.mixins import TwitterSendMixin
from programs.models import Program
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

        address_array = request.POST.get('address_array', '').split(',')
        bioguide_array = request.POST.get('bioguide_array', '').split(',')

        request.session['redirect_url'] = request.META.get('HTTP_REFERER', '/')
        request.session['tweet_text'] = tweet_text
        request.session['sent_tweet'] = False

        request.session['program_id'] = program_id
        request.session['campaign_id'] = campaign_id

        request.session['addressArray'] = address_array
        request.session['bioguiderray'] = bioguide_array
        return resp


class TwitterCallbackView(TwitterSendMixin, OAuthCallbackView):
    """
    Callback view for twitter login. Sends tweet after the user logs in.
    """
    def dispatch(self, request, *args, **kwargs):
        resp = super(TwitterCallbackView, self).dispatch(request, *args, **kwargs)

        if not request.user.is_authenticated():
            messages.error(request, 'Your twitter email address is already taken. Please login into your old account.')
            return HttpResponseRedirect('/accounts/login/')

        self.tweet_text = request.session.get('tweet_text')
        program = request.session.get('program_id')
        self.program = Program.objects.get(pk=program) if program else None
        campaign = request.session.get('campaign_id')
        self.campaign = Campaign.objects.get(slug=campaign) if campaign \
            else None
        request.session['sent_tweet'] = True
        redirect_url = request.session.get('redirect_url')

        if request.user.is_authenticated() and redirect_url and \
                self.tweet_text:
            self.api = self.get_authed_twitter_api()
            if not self.api:
                return HttpResponseRedirect(
                    request.session.get('redirect_url'))
            request.session['alertList'] = json.dumps(
                self.send_tweets_and_generate_response())

            return HttpResponseRedirect(request.session.get('redirect_url'))
        elif redirect_url and not self.tweet_text:
            return HttpResponseRedirect(request.session.get('redirect_url'))
        else:
            return resp

oauth_login = TwitterLoginView.adapter_view(TwitterOAuthAdapter)
oauth_callback = TwitterCallbackView.adapter_view(TwitterOAuthAdapter)


class SaveUserByEmailView(View):
    def post(self, request):
        form = forms.SubscriberEmailForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subscribed!')
        else:
            if form.errors.get('email'):
                messages.success(request, 'Already subscribed!')
            else:
                messages.success(request, 'Invalid email!')
        return redirect('/#email')
