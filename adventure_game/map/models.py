from django.db import models
from django.contrib import auth
from django.contrib.auth.models import User
# Create your models here.


class Level(models.Model):

    user = models.OneToOneField(User,primary_key=True)
    level_number = models.IntegerField(default=0)
    question_number = models.IntegerField(default=1)
    task1_question1_completion = models.BooleanField(default=False)


    def __unicode__(self):
        return str(self.user.username)+"'s current level is '" + str(self.level_number)

class hint(models.Model):

    hint_text = models.CharField(max_length=200)


    def __unicode__(self):
        return 'Hint is <'+str(self.hint_text)+'>'

class QuestionAndAnswer(models.Model):
    hint = models.ForeignKey(hint)
    Question = models.CharField(max_length=200)
    Answer = models.CharField(max_length=200)
    QuestionNumber = models.IntegerField(default=1)
    def __unicode__(self):
        return 'Question #'+str(self.QuestionNumber)+' Question: '+str(self.Question)+'Answer: '+str(self.Answer)
