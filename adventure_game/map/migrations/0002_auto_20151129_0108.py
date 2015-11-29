# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def combine_names(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    hint=apps.get_model("map","hint")
    hint.objects.create(hint_text="888 Madision ave, New York, NY 10021")
    h=hint.objects.get(pk=1)
    questions = apps.get_model("map", "QuestionAndAnswer")
    questions.objects.create(hint=h, Question="What is 3 + 5 = ?",Answer="8",QuestionNumber=1)
    questions.objects.create(hint=h, Question="What is 4 + 4 = ?",Answer="8",QuestionNumber=2)
    questions.objects.create(hint=h, Question="What is 7 + 1 = ?",Answer="8",QuestionNumber=3)
    questions.objects.create(hint=h, Question="What is the 13th letter of the English alphabet?",Answer="m",QuestionNumber=4)
    questions.objects.create(hint=h, Question="What is the 1st letter of the English alphabet?",Answer="a",QuestionNumber=5)
    questions.objects.create(hint=h, Question="What is the 4th letter of the English alphabet?",Answer="d",QuestionNumber=6)
    questions.objects.create(hint=h, Question="What is the 9th letter of the English alphabet?",Answer="i",QuestionNumber=7)
    questions.objects.create(hint=h, Question="What is the 19th letter of the English alphabet?",Answer="s",QuestionNumber=8)
    questions.objects.create(hint=h, Question="What is the 15th letter of the English alphabet?",Answer="o",QuestionNumber=9)
    questions.objects.create(hint=h, Question="What is the 14th letter of the English alphabet?",Answer="n",QuestionNumber=10)


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(combine_names),
    ]
