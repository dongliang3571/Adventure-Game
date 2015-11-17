from django.db import models


class UserProfile(models.Model):
    # user = models.ForeignKey(User, unique=True)
    user = models.OneToOneField(User)
    character = models.CharField(max_length=200)

class PIN(models.Model):
    character = models.ForeignKey(character)
    character_pin = models.CharField(max_length=4, min_length=4)
