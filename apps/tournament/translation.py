from modeltranslation.translator import translator, TranslationOptions
from .models import \
    TournamentRole, \
    AccessToPage


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

translator.register(TournamentRole, RoleTranslationOptions)
translator.register(AccessToPage, AccessTranslationOptions)
