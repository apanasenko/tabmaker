from modeltranslation.translator import translator, TranslationOptions
from .models import \
    AccessToPage, \
    TournamentRole, \
    TournamentStatus


class RoleTranslationOptions(TranslationOptions):
    """
    Класс настроек интернационализации полей модели TournamentRole.
    """

    fields = ('role', )


class AccessTranslationOptions(TranslationOptions):
    """
    Класс настроек интернационализации полей модели AccessToPage.
    """

    fields = ('message', )


class StatusTranslationOptions(TranslationOptions):
    """
    Класс настроек интернационализации полей модели AccessToPage.
    """

    fields = ('name', )

translator.register(TournamentRole, RoleTranslationOptions)
translator.register(AccessToPage, AccessTranslationOptions)
translator.register(TournamentStatus, StatusTranslationOptions)
