from django.conf.urls import patterns, url
from coreapp import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.login, name='login'),
    url(r'^auth/$', views.auth_view, name='auth'),
    url(r'^invalid/$', views.invalid_login),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.registration, name='registration'),
    url(r'^registration-submission/$', views.registration_submission, name='registrationSubmission'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^individual/$',views.individual, name="invidual"),
    url(r'^story/$',views.story, name='story'),
)
