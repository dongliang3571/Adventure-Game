# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0002_auto_20151128_0415'),
    ]

    operations = [
        migrations.AddField(
            model_name='level',
            name='task1_question1_completion',
            field=models.BooleanField(default=False),
        ),
    ]
