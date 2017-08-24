from django.conf.urls import url, include

from . import views


urlpatterns = [
    url(r'^create/$', views.CampaignCreateView.as_view(), name='create'),
    url(r'^delete/(?P<slug>[\w-]+)/$', views.CampaignDeleteView.as_view(), name='delete'),
    url(r'^edit/(?P<slug>[\w-]+)/$', views.CampaignUpdateView.as_view(), name='update'),
    url(r'^list/$', views.CampaignUserListView.as_view(), name='list'),
    url(r'^check/$', views.CheckUrl.as_view(), name='check'),
    url(r'^(?P<slug>[\w-]+)/$', views.CampaignDetailView.as_view(), name='detail'),
]
