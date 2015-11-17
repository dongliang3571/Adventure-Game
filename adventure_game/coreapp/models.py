from django.db import models


class UserProfile(models.Model):
    # user = models.ForeignKey(User, unique=True)
    user = models.OneToOneField(User)
    character = models.CharField(max_length=200)
