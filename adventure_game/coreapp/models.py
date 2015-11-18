from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username

class Character(models.Model):
    user = models.ForeignKey(User)
    character_name = models.CharField(max_length=200)
    character_pin = models.IntegerField(max_length=4, null=True)
    def __str__(self):
		return self.character_name
