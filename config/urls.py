from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url, include
from django.contrib.staticfiles.views import serve as serve_static
from django.views.decorators.cache import never_cache

from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap

from pushthought import views
from programs.sitemaps import ProgramSitemap

from campaigns.views import CampaignDetailView
from actions.views import submit_congress_email_view
from users.views import ProfileView

from .sitemaps import StaticViewSitemap
from .views import LoggedInView, oauth_callback, oauth_login, SaveUserByEmailView


sitemaps = {
    'static': StaticViewSitemap,
    'programs': ProgramSitemap
}

urlpatterns = [
    # Admin
    url(r'^admin/', include(admin.site.urls)),

    url(r'^test/(?P<twitter_screen_name>.*)', views.get_user_by_twitter_screen_name, name='test'),
    url(r'^$', views.HomeView.as_view(), name='home',),
    url(r'^home/$', views.HomeView.as_view(), name='home',),
    url(r'^browse/$', views.browse_view, name='browse'),
    url(r'^browse_campaigns/$', views.browse_campaigns_view, name='browse_campaigns'),
    url(r'^contact_immediately/$', views.ContactImmediatelyView.as_view(), name='contact_immediately'),
    url(r'^campaign_landing/$', views.CampaignLandingView.as_view(), name='campaign_landing'),
    url(r'^email_signup/$', SaveUserByEmailView.as_view(), name='email_signup'),
    url(r'^profile/', ProfileView.as_view(), name='profile'),
    # url(r'^content_landing/(?P<program_id>\w+)/$', views.ContentLandingView.as_view(), name='content_landing'),

    url(r'^accounts/twitter/login/callback/$', oauth_callback, name='twitter_callback'),
    url(r'^accounts/twitter/login/$', oauth_login, name='twitter_login'),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^program/', include('programs.urls', namespace='programs')),
    url(r'^congress/', include('congress.urls', namespace='congress')),
    url(r'^c/', include('campaigns.urls', namespace='campaign')),

    url(r'^is_logged_in/$', LoggedInView.as_view(), name='user_logged_in'),


    url(r'^robots\.txt$', include('robots.urls')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),

    # congress email
    url(r'^submit_congress_email', submit_congress_email_view, name='submit_congress_email_view'),
    url(r'^submit_congress_captcha', views.submit_congress_captcha_view, name='submit_congress_captcha_view'),
    url(r'^submit-email/(?P<email>.*)', views.submit_email, name='submit_email'),
    url(r'^send-contact/', views.send_contact, name='send_contact'),

    url(r'^content_landing/$', views.content_landing_empty, name='content_landing_empty'),
    # url(r'^content_landing/(?P<program_id>\w+)', views.content_landing, name='content_landing'),
    url(r'^get_congress_email_fields', views.get_congress_email_fields_view, name='get_congress_email_fields_view'),
    url(r'^get_congress_with_zip/(?P<zip>\w+)', views.get_congress_with_zip_view, name='get_congress_with_zip'),
    url(r'^get_congress_with_location', views.get_congress_with_location_view, name='get_congress_with_location'),
    # url(r'^get_congress_with_location/(?P<lat>\w+)/(?P<long>\w+)', views.get_congress_with_location_view, name='get_congress_with_location'),
    url(r'^leaving', views.leaving, name='leaving'),
    url(r'^program_detail/(?P<programId>\w+)', views.program_detail, name='program_detail'),
    # url(r'^api', views.api,name='api',),
    # Twitter Verification
    url(r'^verify_twitter', views.verify_twitter),
    # url(r'^verify_twitter/(?P<programId>\w+)/(?P<segmentId>\w+)/(?P<tweet>.*)',
    #     views.verify_twitter),
    url(r'^verify_catch', views.SendTweetView.as_view(),name='verify_catch'),
    # url(r'^store_email_fields_in_session', views.StoreEmailFieldsInSessionView.as_view(),name='store_email_fields_in_session'),


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

urlpatterns += staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += url(r'^static/(?P<path>.*)$', never_cache(serve_static)),
