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
            name='Adventure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('adventure_id', models.CharField(default=b'0000', unique=True, max_length=50)),
                ('adventure_name', models.CharField(max_length=200)),
                ('adventure_description', models.TextField(default=b'', max_length=200, blank=True)),
                ('adventure_img_url', models.URLField(default=b'', blank=True)),
                ('adventure_category', models.CharField(default=b'Outdoor', max_length=10, choices=[(b'Indoor', b'Indoor'), (b'Outdoor', b'Outdoor')])),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choice_1', models.CharField(default=b'', max_length=200, blank=True)),
                ('choice_2', models.CharField(default=b'', max_length=200, blank=True)),
                ('choice_3', models.CharField(default=b'', max_length=200, blank=True)),
                ('choice_4', models.CharField(default=b'', max_length=200, blank=True)),
                ('answer', models.CharField(default=b'5', max_length=10, choices=[(b'1', b'1'), (b'2', b'2'), (b'3', b'3'), (b'4', b'4'), (b'5', b'None from above')])),
            ],
        ),
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
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_type', models.CharField(default=b'Math', max_length=10, choices=[(b'Math', b'Math'), (b'English', b'English'), (b'History', b'History'), (b'Science', b'Science')])),
                ('question_age', models.CharField(default=b'Pre-k', max_length=20, choices=[(b'1. Pre-k', b'Pre-k'), (b'2. Age 4-7', b'Age 4-7'), (b'3. Age 8-10', b'Age 8-10')])),
                ('question_text', models.TextField(default=b'', max_length=200, blank=True)),
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
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_number', models.CharField(default=b'1', max_length=10, choices=[(b'1', b'1'), (b'2', b'2'), (b'3', b'3'), (b'4', b'4'), (b'5', b'5')])),
                ('task_type', models.CharField(default=b'Mission', max_length=10, choices=[(b'Mission', b'Mission'), (b'Questions', b'Questions')])),
                ('task_detail', models.TextField(default=b'', max_length=200, blank=True)),
                ('place_img_url', models.URLField(default=b'', blank=True)),
                ('task_ans', models.CharField(default=b'', max_length=200, blank=True)),
                ('adventure_name', models.ForeignKey(to='map.Adventure')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='question_text',
            field=models.OneToOneField(to='map.Question'),
        ),
    ]
