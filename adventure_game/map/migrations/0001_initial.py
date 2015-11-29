# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='hint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hint_text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('level_number', models.IntegerField(default=0)),
                ('question_number', models.IntegerField(default=1)),
                ('task1_question1_completion', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionAndAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Question', models.CharField(max_length=200)),
                ('Answer', models.CharField(max_length=200)),
                ('QuestionNumber', models.IntegerField(default=1)),
                ('hint', models.ForeignKey(to='map.hint')),
            ],
        ),
    ]
