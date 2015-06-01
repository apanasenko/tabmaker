# -*- coding: utf-8 -*-

__author__ = 'Alexander'


from modeltranslation.translator import translator, TranslationOptions
from .models import TournamentRole


class RoleTranslationOptions(TranslationOptions):
    """
    Класс настроек интернационализации полей модели TournamentRole.
    """

    fields = ('role', )


translator.register(TournamentRole, RoleTranslationOptions)
