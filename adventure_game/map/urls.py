from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.map, name='map'),
    url(r'^beginingstory$', views.beginingstory, name="beginingstory"),
    url(r'^task\d*$', views.task, name="task"),
    # url(r'^scram/$', views.scram, name="task2"),
    url(r'^missiontasksubmission$', views.mission_task_submission, name="missiontasksubmission"),
    url(r'^questionstasksubmission$', views.questions_task_submission, name="questionstasksubmission"),
    url(r'^save_current/$', views.save_current, name="save_current"),
    # url(r'^task1/task1_question2/$', views.task1_question2, name="task1_question2"),
]
