from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class UserProfile(models.Model):
    # user = models.ForeignKey(User, unique=True)
    user = models.OneToOneField(User)

    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username

class Character(models.Model):
    user = models.OneToOneField(User)
    character_name = models.CharField(max_length=200)
    def __str__(self):
		return self.character_name

class PIN(models.Model):
    character_name = models.ForeignKey(Character)
    character_pin = models.IntegerField(validators=[MaxValueValidator(4),MinValueValidator(4)])
