from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username

class Character(models.Model):
    user = models.ForeignKey(User)
    character_name = models.CharField(max_length=200)
    character_pin = models.IntegerField(null=True)

    def __str__(self):
		return self.character_name

    def add_character(self, character, user=user):
        user.character_name.add(character)

    def add_pin(self, pin, user=user, character_name=character_name):
        user.character_pin.add(pin)

    def remove_character(self, character, user=user):
        user.character_name.remove(character)
