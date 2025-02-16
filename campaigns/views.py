from django.views.generic import DetailView, CreateView, DeleteView, View, ListView, UpdateView
from django.http import JsonResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from . import models, forms


class CampaignDetailView(DetailView):
    model = models.Campaign

    def get_queryset(self):
        queryset = super(CampaignDetailView, self).get_queryset()
        return queryset.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super(CampaignDetailView, self).get_context_data(**kwargs)

        if self.request.session.get('alertList'):
            context['alertList'] = self.request.session['alertList']
            del self.request.session['alertList']
        return context


class CampaignUserListView(LoginRequiredMixin, ListView):
    model = models.Campaign

    def get_queryset(self):
        queryset = super(CampaignUserListView, self).get_queryset()
        return queryset.filter(user=self.request.user).order_by('id')


class CampaignDeleteView(DeleteView):
    model = models.Campaign
    success_url = 'campaign:list'

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(CampaignDeleteView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj


    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        success_url = reverse(self.get_success_url())
        self.object.active = not self.object.active
        self.object.save()
        return HttpResponseRedirect(success_url)


class CampaignCreateView(LoginRequiredMixin, CreateView):
    model = models.Campaign
    form_class = forms.CampaignForm

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super(CampaignCreateView, self).form_valid(form)

    def handle_no_permission(self):
        messages.info(self.request,
                      "You must log in to create a campaign.")
        return super(CampaignCreateView, self).handle_no_permission()


class CampaignUpdateView(UpdateView):
    model = models.Campaign
    form_class = forms.CampaignUpdateForm

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(CampaignUpdateView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj


class CheckUrl(LoginRequiredMixin, View):
    def get(self, request):
        slug = request.GET.get('slug')
        current = request.GET.get('current')
        exists = models.Campaign.objects.filter(slug=slug).exists()
        if slug == current:
            exists = False
        return JsonResponse({'result': exists})
