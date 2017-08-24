from django.views.generic import DetailView, CreateView, DeleteView, View, ListView, UpdateView
from django.http import JsonResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin

from . import models, forms


class CampaignDetailView(DetailView):
    model = models.Campaign


class CampaignUserListView(LoginRequiredMixin, ListView):
    model = models.Campaign

    def get_queryset(self):
        queryset = super(CampaignUserListView, self).get_queryset()
        return queryset.filter(user=self.request.user)


class CampaignDeleteView(DeleteView):
    model = models.Campaign
    success_url = 'campaign:list'

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(CampaignDeleteView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj


class CampaignCreateView(LoginRequiredMixin, CreateView):
    model = models.Campaign
    form_class = forms.CampaignForm

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super(CampaignCreateView, self).form_valid(form)


class CampaignUpdateView(UpdateView):
    model = models.Campaign
    form_class = forms.CampaignForm

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(CampaignUpdateView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj


class CheckUrl(LoginRequiredMixin, View):
    def get(self, request):
        slug = request.GET.get('slug')
        exists = models.Campaign.objects.filter(slug=slug).exists()
        return JsonResponse({'result': exists})