from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.map, name='map'),
    url(r'^task1/$',views.task1, name="task1"),
]
