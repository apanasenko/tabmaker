from django.db import models

from . round import Round
from . profile import User
from . tournament import Tournament


class CustomFormType(models.Model):
    name = models.CharField(max_length=100)


class CustomFieldAlias(models.Model):
    name = models.CharField(max_length=100)


class CustomForm(models.Model):
    tournament = models.ForeignKey(Tournament)
    form_type = models.ForeignKey(CustomFormType)

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
    form = models.ForeignKey(CustomForm)
    alias = models.ForeignKey(CustomFieldAlias, blank=True, null=True)


class CustomFormAnswers(models.Model):
    form = models.ForeignKey(CustomForm)
    answers = models.TextField()

    @staticmethod
    def save_answer(custom_form, answers):
        import json
        return CustomFormAnswers.objects.create(form=custom_form, answers=json.dumps(answers))

    @staticmethod
    def get_answers(custom_form):
        import json
        return list(map(
            lambda x: json.loads(x.answers),
            CustomFormAnswers.objects.filter(form=custom_form).order_by('id')
        ))


class FeedbackAnswer(CustomFormAnswers):
    user = models.ForeignKey(User)
    round = models.ForeignKey(Round)
