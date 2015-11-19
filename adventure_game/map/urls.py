from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='map'),
    url(r'^task1/$',views.task1, name="task1"),
    url(r'^task2/$',views.task2, name="task2"),
    url(r'^task1/task1_question1/$',views.task1_question1, name="task1_question1"),
]
