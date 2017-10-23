# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import UpdateView
from django.contrib.messages.views import SuccessMessageMixin

from . import forms


class ProfileView(SuccessMessageMixin, UpdateView):
    form_class = forms.ProfileForm
    template_name = 'users/profile_form.html'
    success_url = '/profile/'
    success_message = 'Zip code saved!'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            request.session['zip'] = form.cleaned_data['zip']
        return super(ProfileView, self).post(request, *args, **kwargs)
