from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^map$', views.map, name='map'),
    url(r'^story$', views.story, name="story"),
    url(r'^task\d*$', views.task, name="task"),
    # url(r'^task2/$', views.task2, name="task2"),
    url(r'^tasksubmission', views.Task_Submission, name="tasksubmission")
    # url(r'^task1/task1_question1/$', views.task1_question1, name="task1_question1"),
    # url(r'^task1/task1_question2/$', views.task1_question2, name="task1_question2"),
]
