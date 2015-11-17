from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class UserProfile(models.Model):
    # user = models.ForeignKey(User, unique=True)
    user = models.OneToOneField(User)
    character = models.CharField(max_length=200)

class PIN(models.Model):
    character = models.ForeignKey(UserProfile)
    character_pin = models.IntegerField(validators=[MaxValueValidator(100),MinValueValidator(1)])
