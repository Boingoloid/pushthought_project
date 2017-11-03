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
# from django.conf.urls import (
# handler400, handler403, handler404, handler500
# )
# # handler400 = 'views.bad_request'
# # handler403 = 'views.permission_denied'
# handler404 = 'views.page_not_found'
# # handler500 = 'views.server_error'

from django.conf.urls import url, include
from snippets import urls
from actions.views import SubmitCongressEmail
import views


urlpatterns = [
    # url(r'^test/(?P<twitter_screen_name>.*)', views.get_user_by_twitter_screen_name,name='test',),
    url(r'^home', views.home,name='home',),


    # This line added to cut off all urls to home
    # url(r'^.*$', views.home,name='home',),

    url(r'^$', views.home,name='home'),
    # congress email
    url(r'^submit_congress_captcha', views.submit_congress_captcha_view,name='submit_congress_captcha_view'),
    url(r'^submit-email/(?P<email>.*)', views.submit_email,name='submit_email'),
    url(r'^send-contact/', views.send_contact,name='send_contact'),
    url(r'^browse', views.browse, name='browse'),
    # url(r'^content_landing/$', views.content_landing_empty, name='content_landing_empty'),
    # url(r'^content_landing/(?P<segment_id>\w+)', views.content_landing, name='content_landing'),
    url(r'^get_congress_email_fields', views.get_congress_email_fields_view, name='get_congress_email_fields_view'),
    url(r'^get_congress_with_zip/(?P<zip>\w+)', views.get_congress_with_zip_view, name='get_congress_with_zip'),
    url(r'^get_congress_with_location', views.get_congress_with_location_view,
        name='get_congress_with_location'),
    # url(r'^get_congress_with_location/(?P<lat>\w+)/(?P<long>\w+)', views.get_congress_with_location_view, name='get_congress_with_location'),
    url(r'^leaving', views.leaving, name='leaving'),
    url(r'^program_detail/(?P<programId>\w+)', views.program_detail, name='program_detail'),
    # url(r'^api', views.api,name='api',),
    # Twitter Verification
    url(r'^verify_twitter',views.verify_twitter),
    # url(r'^verify_twitter/(?P<programId>\w+)/(?P<segmentId>\w+)/(?P<tweet>.*)',
    #     views.verify_twitter),
    url(r'^verify_catch', views.SendTweetView.as_view(), name='verify_catch'),

    # Admin
    url(r'^admin', include(admin.site.urls)),

    # Backburner
    url(r'^snippets', include('snippets.urls')),
    url(r'^prime', include('prime.urls')),
    # url(r'^account/(?P<user_pk>\d+)/(?P<program_pk>\d+)/addsegment', views.add_segment, name='add_segment'),
    # url(r'^account/(?P<user_pk>\d+)/(?P<program_pk>\d+)/(?P<segment_pk>\d+)', views.segment_menu, name='segment_menu'),
    # url(r'^account/(?P<user_pk>\d+)/(?P<program_pk>\d+)', views.segment_list, name='segment_list'),

    #account home
    url(r'^account/(?P<user_pk>\w+)', views.account_home, name='account_home'),

    # Action Menu
    url(r'^action_menu/(?P<programId>\w+)/(?P<segmentId>\w+)/fed_representative',views.fed_rep_action_menu),
    url(r'^action_menu/(?P<programId>\w+)/(?P<segmentId>\w+)/petition',views.petition),
    url(r'^action_menu/(?P<programId>\w+)/(?P<segmentId>\w+)/communication',views.petition),
    url(r'^action_menu/(?P<programId>\w+)/(?P<segmentId>\w+)',views.action_menu),
    url(r'^user_signin_form',views.user_signin_form, name='user_signin_form'),
    url(r'^login_form',views.login_form, name='login_form'),
    url(r'^logout', views.user_logout, name='user_logout'),



    # segment JPGM9mmcKV   program JPGM9mmcKV
    # url(r'^action_menu/(?P<segment_pk>\d+)/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})', views.action_menu,
    # url(r'^action_menu/(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})-(<segment_name>)', views.action_menu, name='action_menu'),

    url(r'^about',views.about, name='about'),
    # url(r'^register', views.register, name='register'),
    # url(r'^login', views.user_login, name='login'),
    url(r'^contact',views.contact,name='contact'),
    #url(r'^pushthought/', views.), # ADD THIS NEW TUPLE!
    #url(r'^programs/', include('pushthought.urls')),
    # url(r'^accounts/', include('registration.backends.default.urls')),

    #potentially comment out line above
]

urlpatterns += staticfiles_urlpatterns()

from django.conf import settings
from django.contrib.staticfiles.views import serve as serve_static
from django.views.decorators.cache import never_cache


if settings.DEBUG:
    urlpatterns += url(r'^static/(?P<path>.*)$', never_cache(serve_static)),
