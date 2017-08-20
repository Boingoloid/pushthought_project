from django.views.generic import DetailView, CreateView, View
from django.http import JsonResponse

from . import models, forms


class CampaignDetailView(DetailView):
    model = models.Campaign
    slug_field = 'slug'
    template_name = 'campaign_landing.html'


class CampaignCreateView(CreateView):
    template_name = 'create_campaign.html'
    model = models.Campaign

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super(CampaignCreateView, self).form_valid(form)

    form_class = forms.CampaignForm

    def get_context_data(self, **kwargs):
        context = super(CampaignCreateView, self).get_context_data(**kwargs)

        return context


class CheckUrl(View):
    def get(self, request):
        slug = request.GET.get('slug')
        exists = models.Campaign.objects.filter(slug=slug).exists()
        return JsonResponse({'result': exists})