from django import forms

from . import models


class CampaignForm(forms.ModelForm):
    class Meta:
        model = models.Campaign
        exclude = ('user', 'active', 'counter')
