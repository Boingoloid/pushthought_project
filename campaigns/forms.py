from django import forms

from . import models


class CampaignForm(forms.ModelForm):
    class Meta:
        model = models.Campaign
        fields = ('slug', 'title', 'description', 'image', 'tweet_text', 'email_text', 'link', )


class CampaignUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Campaign
        fields = ('title', 'description', 'image', 'tweet_text', 'email_text', 'link',)
