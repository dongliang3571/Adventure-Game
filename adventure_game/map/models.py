from django.db import models
from django.contrib import auth
from django.contrib.auth.models import User
# Create your models here.


class Level(models.Model):

    user = models.OneToOneField(User,primary_key=True)
    level_number = models.IntegerField(default=0)


    def __unicode__(self):
        return str(self.user.username)+"'s current level is '" + str(self.level_number)


class QuestionAndAnswer(models.Model):

    Question = models.CharField(max_length=200)
    Answer = models.CharField(max_length=200)

    def __unicode__(self):
        return 'Question: '+str(self.Question)+'Answer: '+str(self.Answer)
