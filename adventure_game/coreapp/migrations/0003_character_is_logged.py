# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coreapp', '0002_auto_20151125_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='is_logged',
            field=models.BooleanField(default=False),
        ),
    ]
