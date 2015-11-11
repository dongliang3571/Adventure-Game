from django.conf.urls import patterns, url
from coreapp import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.login, name='login'),
    url(r'^auth/$', views.auth_view, name='auth'),
    url(r'^invalid/$', views.invalid_login),
    url(r'^logout/$', views.logout),
)
