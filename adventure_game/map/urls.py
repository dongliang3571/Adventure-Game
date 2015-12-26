from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.map, name='map'),
    url(r'^beginingstory$', views.beginingstory, name="beginingstory"),
    url(r'^task\d*$', views.task, name="task"),
    url(r'^missiontasksubmission$', views.mission_task_submission, name="missiontasksubmission"),
    url(r'^questionstasksubmission$', views.questions_task_submission, name="questionstasksubmission"),
    url(r'^save_current/$', views.save_current, name="save_current"),
    url(r'^special_game_json/$', views.special_game_json, name="special_game_json"),
    url(r'^visitorview$', views.visitorview, name="visitorview"),
]
