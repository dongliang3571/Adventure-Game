# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coreapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='current_adventures',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('adventure_saved', models.CharField(default=b'', max_length=10, blank=True)),
                ('task_saved', models.CharField(default=b'', max_length=10, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
