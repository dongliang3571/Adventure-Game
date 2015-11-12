from django.db import models

# Create your models here.

class Level(models.Model):
    level_number = models.IntegerField(default=0)

    def __unicode__(self):
        return "Current level is " + str(self.level_number)
