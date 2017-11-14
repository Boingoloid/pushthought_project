import tweepy
import re

from allauth.compat import reverse
from allauth.socialaccount.models import SocialApp, SocialToken


from django.contrib import messages
from django.http.response import JsonResponse
from django.contrib.sites.shortcuts import get_current_site

from actions.models import Action
from congress.models import Congress
from campaigns.models import Campaign


class TwitterSendMixin(object):
    """
    Twitter functions to send a tweet.
    """

    def get_authed_twitter_api(self):
        try:
            token_obj = SocialToken.objects.get(account__user=self.request.user, account__provider='twitter')
        except SocialToken.DoesNotExist:
            messages.error(self.request, 'Please, log out and log in through Twitter to send a tweet.')
            return

        TWITTER_CONSUMER_SECRET = SocialApp.objects.filter(provider='twitter').last().secret
        TWITTER_CONSUMER_KEY = SocialApp.objects.filter(provider='twitter').last().client_id

        auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_access_token(token_obj.token, token_obj.token_secret)
        api = tweepy.API(auth)
        return api

    def get_mentions(self):
        return self.request.session.get('addressArray', [])

    def get_clean_tweet_text(self):
        pattern = r'@\w+,?\s'
        replacement = ''
        clean_text = re.sub(pattern, replacement, self.tweet_text)
        return clean_text.encode('utf-8')

    # def get_url(self):
    #     url = 'pushthought.com'
    #     if self.program:
    #         url += reverse('programs:detail', kwargs={'pk': self.program})
    #     elif self.campaign:
    #         url += reverse('campaign:detail', kwargs={'slug': self.campaign})
    #     else:
    #         url = ''
    #
    #     return url

    # def get_tweet_text_with_url(self):
    #     url = self.get_url()
    #     tweet_text_with_url = '{} {}'.format(self.get_clean_tweet_text(), url)
    #
    #     return tweet_text_with_url

    def send_tweet(self, mention, text):
        try:
            congress = Congress.objects.get(twitter=mention)
        except Congress.DoesNotExist:
            return 'unknown_congressman'
        tweet_text_with_metion = '@{} {}'.format(mention, text)

        if len(tweet_text_with_metion) > 140:
            return 'too_long'

        try:
            self.api.update_status(tweet_text_with_metion)
            if self.program:
                Action.tweets.create(tweet_text_with_metion,
                                     user=self.request.user,
                                     program_id=self.program,
                                     congress=congress)
            elif self.campaign:
                campaign = Campaign.objects.get(slug=self.campaign)
                Action.tweets.create(tweet_text_with_metion,
                                     user=self.request.user,
                                     campaign=campaign,
                                     congress=congress)
            return 'success'
        except tweepy.TweepError as e:
            if e.api_code == 187:
                return 'duplicate'
            return 'error'

    def send_tweets(self, mentions, text):
        return {mention: self.send_tweet(mention, text)
                for mention in mentions}

    def send_tweets_and_generate_response(self):
        self.api = self.get_authed_twitter_api()
        mentions = self.get_mentions()
        if not mentions:
            return {'status': 'no_mentions'}
        statuses = self.send_tweets(mentions, self.get_clean_tweet_text())

        successes = [s for s in statuses.values() if s == 'success']
        if len(successes) == len(statuses):
            status = 'success'
        elif successes:
            status = 'partial_success'
        else:
            status = 'error'
        return {'status': status, 'statuses': statuses}
