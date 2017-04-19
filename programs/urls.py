from django.conf.urls import url, include

from . import views


urlpatterns = [
    url(r'^(?P<pk>\d+)$', views.ProgramDetailView.as_view(), name='detail'),
    url(r'^search/imdb/id/$', views.SearchIMDBProgramIDView.as_view(), name='search_imdb_id'),
]
