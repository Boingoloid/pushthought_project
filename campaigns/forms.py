from django import forms

from twitter_text.validation import Validation as TweetValidation

from . import models


class CampaignEditingBaseForm(forms.ModelForm):
    TWEET_MAX_LENGTH = 280
    # Max username length is 15, plus "@" before and a space after.
    TWEET_MENTION_PLACEHOLDER_LENGTH = 17

    def clean_tweet_text(self):
        value = self.cleaned_data['tweet_text']
        if TweetValidation(value).tweet_length() + \
                self.TWEET_MENTION_PLACEHOLDER_LENGTH > self.TWEET_MAX_LENGTH:
            raise forms.ValidationError("Too long.")
        return value


class CampaignForm(CampaignEditingBaseForm):
    class Meta:
        model = models.Campaign
        fields = ('slug', 'title', 'description', 'image', 'tweet_text', 'email_text', 'link', )
        widgets = {
            'link': forms.widgets.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super(CampaignForm, self).__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].widget.attrs['class'] = '{0} {1}'.format('field-input', 'field-input-'+name)
        self.fields['slug'].error_messages['unique'] = \
            'That url is already taken.'

    def clean(self):
        cleaned_data = super(CampaignForm, self).clean()
        tweet = cleaned_data.get("tweet_text")
        email = cleaned_data.get("email_text")
        if not tweet and not email:
            # Only do something if both fields are empty.
            raise forms.ValidationError(
                "Please fill out suggested text for email, tweet, or both."
            )

class CampaignUpdateForm(CampaignEditingBaseForm):
    class Meta:
        model = models.Campaign
        fields = ('title', 'description', 'image', 'tweet_text', 'email_text', 'link',)
        widgets = {
            'link': forms.widgets.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super(CampaignUpdateForm, self).__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].widget.attrs['class'] = '{0} {1}'.format('field-input', 'field-input-'+name)

    def clean(self):
        cleaned_data = super(CampaignUpdateForm, self).clean()
        tweet = cleaned_data.get("tweet_text")
        email = cleaned_data.get("email_text")
        if not tweet and not email:
            # Only do something if both fields are empty.
            raise forms.ValidationError(
                "Please fill out suggested text for email, tweet, or both."
            )
