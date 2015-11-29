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
