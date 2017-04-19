from django.conf.urls import url, include

from . import views


urlpatterns = [
    url(r'^(?P<pk>\d+)$', views.ProgramDetailView.as_view(), name='detail'),
    url(r'^add/imdb/id/$', views.SearchIMDBProgramIDView.as_view(), name='add_imdb_id'),
    url(r'^search/imdb/name/$', views.SearchIMDBProgramTitleView.as_view(), name='search_imdb_title'),
]
