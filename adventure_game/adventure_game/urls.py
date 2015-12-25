"""This module is used to route the urls to the views
"""

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('coreapp.urls', namespace="coreapp")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^adventure\d*/', include('map.urls', namespace="map")),
]
