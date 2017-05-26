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
from actions.views import submit_congress_email_view

from .sitemaps import StaticViewSitemap
from .views import LoggedInView, oauth_callback, oauth_login


sitemaps = {
    'static': StaticViewSitemap,
    'programs': ProgramSitemap
}

urlpatterns = [
    # Admin
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.HomeView.as_view(), name='home',),
    url(r'^home/$', views.HomeView.as_view(), name='home',),
    url(r'^browse/$', views.BrowseView.as_view(), name='browse'),

    url(r'^accounts/twitter/login/callback/$', oauth_callback, name='twitter_callback'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^program/', include('programs.urls', namespace='programs')),
    url(r'^congress/', include('congress.urls', namespace='congress')),

    url(r'^robots\.txt$', include('robots.urls')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),

    # congress email
    url(r'^get_congress_email_fields', views.get_congress_email_fields_view, name='get_congress_email_fields_view'),
    url(r'^submit_congress_email', submit_congress_email_view, name='submit_congress_email_view'),
    url(r'^submit_congress_captcha', views.submit_congress_captcha_view, name='submit_congress_captcha_view'),
    url(r'^submit-email/(?P<email>.*)', views.submit_email, name='submit_email'),
    url(r'^send-contact/', views.send_contact, name='send_contact'),

    url(r'^verify_catch', views.SendTweetView.as_view(),name='verify_catch'),
    url(r'^save_tweet_twitter_login/$', oauth_login, name='save_tweet_twitter_login'),


    url(r'^about',views.about, name='about'),
    url(r'^contact',views.contact,name='contact'),
]

urlpatterns += staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += url(r'^static/(?P<path>.*)$', never_cache(serve_static)),
