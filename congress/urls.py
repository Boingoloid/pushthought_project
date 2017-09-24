from django.conf.urls import url, include

from . import views


urlpatterns = [
    url(r'^add_zip/(?P<zip_code>\d+)/$', views.GetCongressData.as_view(), name='add_zip'),
    url(r'^campaign/add_zip/(?P<zip_code>\d+)/$', views.GetCongressCampaignData.as_view(), name='add_zip_campaign'),
    url(r'^add_location/$', views.GetCongressDataLocation.as_view(), name='add_location'),
]
