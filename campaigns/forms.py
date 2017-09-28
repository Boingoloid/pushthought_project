from django import forms

from . import models


class CampaignForm(forms.ModelForm):
    class Meta:
        model = models.Campaign
        fields = ('slug', 'title', 'description', 'image', 'tweet_text', 'email_text', 'link', )

    def __init__(self, *args, **kwargs):
        super(CampaignForm, self).__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].widget.attrs['class'] = '{0} {1}'.format('field-input', 'field-input-'+name)
        self.fields['slug'].error_messages = {'unique': 'That url is already taken.'}

    def clean(self):
        cleaned_data = super(CampaignForm, self).clean()
        tweet = cleaned_data.get("tweet_text")
        email = cleaned_data.get("email_text")
        print "*****CLEANING*****************"
        if not tweet and not email:
            print "*****VALIDATION ERROR*****************"
            # Only do something if both fields are empty.
            raise forms.ValidationError(
                "Please fill out suggested text for email, tweet, or both."
            )

class CampaignUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Campaign
        fields = ('title', 'description', 'image', 'tweet_text', 'email_text', 'link',)

    def __init__(self, *args, **kwargs):
        super(CampaignUpdateForm, self).__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].widget.attrs['class'] = '{0} {1}'.format('field-input', 'field-input-'+name)
        # self.fields['slug'].error_messages = {'unique': 'That url is already taken.'}

    def clean(self):
        cleaned_data = super(CampaignUpdateForm, self).clean()
        tweet = cleaned_data.get("tweet_text")
        email = cleaned_data.get("email_text")
        print "*****CLEANING*****************"
        if not tweet and not email:
            print "*****VALIDATION ERROR*****************"
            # Only do something if both fields are empty.
            raise forms.ValidationError(
                "Please fill out suggested text for email, tweet, or both."
            )
