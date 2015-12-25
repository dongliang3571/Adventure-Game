from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username

class Character(models.Model):
    """
    This holds family members in database. A family member has a name and pin number that need to go to their own profile page.
    """
    user = models.ForeignKey(User)
    character_name = models.CharField(max_length=200)
    character_pin = models.CharField(max_length=200,null=True)
    is_logged = models.BooleanField(default=False)

    def __str__(self):
        return self.character_name

#############################################
class Level_num(models.Model):
    """
    Each user has game points which can be gained from our games. A user's level is determined by their points.
    """
    user = models.OneToOneField(User)
    user_point = models.PositiveIntegerField(default=0)
    user_level_choices = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    user_level = models.IntegerField(choices = user_level_choices, default='1')

    def __unicode__(self):
        return str(self.user_level)


class Track(models.Model):
    """
    This holds a list of adventures that a user has completed.
    """
    user = models.ForeignKey(User)
    adventure_done = models.CharField(max_length=10, blank=True, default='')

    def __unicode__(self):
        return self.adventure_done


class Game_saved(models.Model):
    """
    This saves the progress of a game.
    """
    user = models.OneToOneField(User)
    adventure_saved = models.CharField(max_length=10, blank=True, default='')  #adventure_id
    task_saved = models.CharField(max_length=10, blank=True, default='')   #task_number

    def __unicode__(self):
        return 'Last saved at adventure id#'+str(self.adventure_saved) + 'task #:' + str(self.task_saved)

class current_adventures(models.Model):
    """
    This saves users' adventures that are currently played.
    """
    user = models.ForeignKey(User)
    adventure_saved = models.CharField(max_length=10, blank=True, default='')  #adventure_id
    task_saved = models.CharField(max_length=10, blank=True, default='')   #task_number

    def __unicode__(self):
        return 'saved adventure id#'+str(self.adventure_saved) + 'task #:' + str(self.task_saved)

class ContactUs(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    msg = models.TextField(max_length=2000)
