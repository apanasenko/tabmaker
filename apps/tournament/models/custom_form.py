from django.db import models

from . round import Round
from . profile import User
from . tournament import Tournament

import json


class CustomFormType(models.Model):
    name = models.CharField(max_length=100)


class CustomFieldAlias(models.Model):
    name = models.CharField(max_length=100)


class CustomForm(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    form_type = models.ForeignKey(CustomFormType, on_delete=models.CASCADE)

    @staticmethod
    def get_or_create(tournament: Tournament, form_type: CustomFormType):
        from ..consts import CUSTOM_FIELD_SETS

        form = CustomForm.objects.get_or_create(tournament=tournament, form_type=form_type)
        if form[1] and form_type in CUSTOM_FIELD_SETS:  # is create
            fields = CUSTOM_FIELD_SETS[form_type]
            for i in range(len(fields)):
                CustomQuestion.objects.create(
                    question=fields[i][1],
                    comment='',
                    position=(i + 1),
                    required=fields[i][2],
                    form=form[0],
                    alias=fields[i][0]
                )

        return form[0]


class CustomQuestion(models.Model):
    question = models.CharField(max_length=300)
    comment = models.TextField()
    position = models.PositiveIntegerField()
    required = models.BooleanField(default=True)
    form = models.ForeignKey(CustomForm, on_delete=models.CASCADE)
    alias = models.ForeignKey(CustomFieldAlias, blank=True, null=True, on_delete=models.SET_NULL)


class CustomFormAnswers(models.Model):
    form = models.ForeignKey(CustomForm, on_delete=models.CASCADE)
    answers = models.TextField()

    def set_answers(self, answers):
        self.answers = json.dumps(answers)

    def get_answers(self):
        return json.loads(self.answers)


class FeedbackAnswer(CustomFormAnswers):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
