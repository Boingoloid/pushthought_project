"""pushthought URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.conf.urls import url, include
from snippets import urls
from . import views

urlpatterns = [
    url(r'^action_menu/verify_twitter/(?P<tweet_text>\w+)',views.verify_twitter_with_tweet),
    url(r'^action_menu/verify_twitter/',views.verify_twitter, name='verify_twitter'),
    url(r'^verify_catch', views.verify_catch,name='verify_catch'),
    url(r'^admin', include(admin.site.urls)),
    url(r'^snippets', include('snippets.urls')),
    url(r'^prime', include('prime.urls')),
    url(r'^account/(?P<user_pk>\d+)/(?P<program_pk>\d+)/addsegment', views.add_segment, name='add_segment'),
    url(r'^account/(?P<user_pk>\d+)/(?P<program_pk>\d+)/(?P<segment_pk>\d+)', views.segment_menu, name='segment_menu'),
    url(r'^account/(?P<user_pk>\d+)/(?P<program_pk>\d+)', views.segment_list, name='segment_list'),
    url(r'^account/(?P<user_pk>\d+)', views.account_home, name='account_home'),
    url(r'^action_menu/(?P<programId>\w+)/(?P<segmentId>\w+)/fed_representative',views.fed_rep_action_menu),
    url(r'^action_menu/(?P<programId>\w+)/(?P<segmentId>\w+)',views.action_menu),
    # segment JPGM9mmcKV   program JPGM9mmcKV
    # url(r'^action_menu/(?P<segment_pk>\d+)/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})', views.action_menu,
     # url(r'^action_menu/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})-(<segment_name>)', views.action_menu, name='action_menu'),
    # url(r'^logout', views.user_logout, name='auth_logout'),
    url(r'^about',views.about, name='about'),
    # url(r'^register', views.register, name='register'),
    # url(r'^login', views.user_login, name='login'),
    url(r'^contact',views.contact,name='contact'),
    #url(r'^pushthought/', views.), # ADD THIS NEW TUPLE!
    #url(r'^programs/', include('pushthought.urls')),

    # url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^home', views.home,name='home',),
    # url(r'^api', views.api,name='api',),
    url(r'^$', views.home,name='home'),
    #potentially comment out line above
]

urlpatterns += staticfiles_urlpatterns()