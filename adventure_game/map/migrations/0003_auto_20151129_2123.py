# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0002_auto_20151129_0108'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adventure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('adventure_name', models.CharField(max_length=200)),
                ('adventure_description', models.TextField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('answer', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Hints',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('hints', models.CharField(max_length=200)),
                ('question', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('task', models.CharField(max_length=200)),
                ('task_details', models.TextField(max_length=200)),
                ('hint', models.CharField(max_length=200, null=True)),
                ('adventure_name', models.ForeignKey(to='map.Adventure')),
            ],
        ),
        migrations.AddField(
            model_name='hints',
            name='task',
            field=models.ForeignKey(to='map.Task'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='map.Hints'),
        ),
    ]
