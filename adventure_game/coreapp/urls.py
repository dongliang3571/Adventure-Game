from django.conf.urls import url
from coreapp import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^auth/$', views.auth_view, name='auth'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.registration, name='registration'),
    url(r'^registration-submission/$', views.registration_submission, name='registrationSubmission'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^individual/$',views.individual, name="individual"),
    url(r'^story/$',views.story, name='story'),
    url(r'^add-familly-member-submission/$',views.add_family_member_submission, name="addFamilySubmission"),
    url(r'^add-family-member/$',views.add_family_member,name="add-family-member"),
]
