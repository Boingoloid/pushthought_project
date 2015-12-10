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

from . import views

urlpatterns = [
    url(r'(?P<user_pk>\d+)/(?P<program_pk>\d+)/addsegment', views.add_segment, name='add_segment'),
    url(r'(?P<user_pk>\d+)/(?P<program_pk>\d+)/(?P<segment_pk>\d+)', views.segment_menu, name='segment_menu'),
    url(r'(?P<user_pk>\d+)/(?P<program_pk>\d+)', views.segment_list, name='segment_list'),
    url(r'(?P<user_pk>\d+)', views.account_home, name='account_home'),
    url(r'^logout', views.user_logout, name='logout'),
    url(r'^about',views.about, name='about'),
    url(r'^register', views.register, name='register'),
    url(r'^login', views.user_login, name='login'),
    url(r'^contact',views.contact,name='contact'),
    #url(r'^pushthought/', views.), # ADD THIS NEW TUPLE!
    #url(r'^programs/', include('pushthought.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^$', views.home,name='home',),
]

urlpatterns += staticfiles_urlpatterns()
