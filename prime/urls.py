from django.conf.urls import url
from prime import views

urlpatterns = [
    url(r'^prime/$', views.segmentapi_list),
    url(r'^prime/(?P<pk>[0-9]+)/$', views.segmentapi_detail),
]