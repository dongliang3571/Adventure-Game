# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='id_of_task',
            field=models.CharField(default=b'', max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='name_of_location',
            field=models.CharField(default=b'', max_length=2000, blank=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_ans',
            field=models.CharField(default=b'', max_length=2000, blank=True),
        ),
    ]
