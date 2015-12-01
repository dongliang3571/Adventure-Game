from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username

class Character(models.Model):
    user = models.ForeignKey(User)
    character_name = models.CharField(max_length=200)
    character_pin = models.CharField(max_length=200,null=True)
    is_logged = models.BooleanField(default=False)

    def __str__(self):
        return self.character_name

#############################################
class Level(models.Model):
    user = models.ForeignKey(User)
    user_point = models.PositiveIntegerField(default=0)
    user_level_choices = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    user_level = models.IntegerField(choices = user_level_choices, default='1')

    def __unicode__(self):
        return self.user_level


class Track(models.Model):
    user = models.ForeignKey(User)
    adventures_done = models.CharField(blank=True, default='')

    def __unicode__(self):
        return self.adventures_done


class Game_saved(models.Model):
    user = models.ForeignKey(User)
    adventure_saved = models.CharField(blank=True, default='')  #adventure_id
    task_saved = models.CharField(blank=True, default='')   #task_number

    def __unicode__(self):
        return 'Last saved at adventure id#'+str(self.adventure_saved) + 'task #:' + str(self.task_saved)
