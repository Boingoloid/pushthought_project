from django.conf.urls import url, include

from . import views


urlpatterns = [
    url(r'^create/$', views.CampaignCreateView.as_view(), name='create'),
    url(r'^check/$', views.CheckUrl.as_view(), name='check'),
    url(r'^(?P<slug>[\w-]+)/$', views.CampaignDetailView.as_view(), name='detail'),
]
