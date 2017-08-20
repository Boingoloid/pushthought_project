from django.views.generic import DetailView, CreateView

from . import models, forms


class CampaignDetailView(DetailView):
    model = models.Campaign
    slug_field = 'slug'
    template_name = 'campaign_landing.html'


class CampaignCreateView(CreateView):
    template_name = 'create_campaign.html'
    model = models.Campaign
    form_class = forms.CampaignForm

    def get_context_data(self, **kwargs):
        context = super(CampaignCreateView, self).get_context_data(**kwargs)

        return context