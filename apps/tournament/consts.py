from enum import Enum
from .messages import *
from .models import \
    CustomFormType, \
    CustomFieldAlias, \
    TournamentRole, \
    TournamentStatus

TEAM_IN_GAME = 4
POINTS_OF_FIRST_PLACE = 3
POINTS_OF_SECOND_PLACE = 2

Position = Enum('Position', 'OG OO CG CO NONE')

ROLE_OWNER = TournamentRole.objects.get(role_en='Owner')
ROLE_ADMIN = TournamentRole.objects.get(role_en='Admin')
ROLE_CHIEF_ADJUDICATOR = TournamentRole.objects.get(role_en='Chief adjudicator')

ROLE_TEAM_REGISTERED = TournamentRole.objects.get(role_en='Registered')
ROLE_IN_TAB = TournamentRole.objects.get(role_en='In tab')
ROLE_WAIT_LIST = TournamentRole.objects.get(role_en='Wait list')
ROLE_VERIFIED = TournamentRole.objects.get(role_en='Verified')  # Участник подтвердил участие
ROLE_APPROVED = TournamentRole.objects.get(role_en='Approved')  # Организатор подтвердил
ROLE_MEMBER = TournamentRole.objects.get(role_en='Member')

ROLE_ADJUDICATOR_REGISTERED = TournamentRole.objects.get(role_en='Registered adjudicator')
ROLE_ADJUDICATOR_APPROVED = TournamentRole.objects.get(role_en='Approved adjudicator')
ROLE_WING = TournamentRole.objects.get(role_en='Wing')
ROLE_CHAIR = TournamentRole.objects.get(role_en='Chair')

STATUS_REGISTRATION = TournamentStatus.objects.get(name_en='Registration open')
STATUS_PREPARATION = TournamentStatus.objects.get(name_en='Registration closed')
STATUS_STARTED = TournamentStatus.objects.get(name_en='Qualification')
STATUS_PLAYOFF = TournamentStatus.objects.get(name_en='Playoff')
STATUS_FINISHED = TournamentStatus.objects.get(name_en='Finished')

TEAM_ROLES_NAMES = [
    'Registered',
    'In tab',
    'Wait list',
    'Verified',
    'Approved',
    'Member',
]

ADJUDICATOR_ROLES_NAMES = [
    'Registered adjudicator',
    'Approved adjudicator',
    'Wing',
    'Chair',
]

TEAM_ROLES = TournamentRole.objects.filter(role_en__in=TEAM_ROLES_NAMES)
ADJUDICATOR_ROLES = TournamentRole.objects.filter(role_en__in=ADJUDICATOR_ROLES_NAMES)

FORM_REGISTRATION_TYPE = CustomFormType.objects.get(name='registration')
FORM_FEEDBACK_TYPE = CustomFormType.objects.get(name='feedback')

FIELD_ALIAS_SPEAKER_1 = CustomFieldAlias.objects.get(name='speaker_1_email')
FIELD_ALIAS_SPEAKER_1_F_NAME = CustomFieldAlias.objects.get(name='speaker_1_first_name')
FIELD_ALIAS_SPEAKER_1_L_NAME = CustomFieldAlias.objects.get(name='speaker_1_last_name')
FIELD_ALIAS_SPEAKER_1_UNIVERSITY = CustomFieldAlias.objects.get(name='speaker_1_university')
FIELD_ALIAS_SPEAKER_2 = CustomFieldAlias.objects.get(name='speaker_2_email')
FIELD_ALIAS_SPEAKER_2_F_NAME = CustomFieldAlias.objects.get(name='speaker_2_first_name')
FIELD_ALIAS_SPEAKER_2_L_NAME = CustomFieldAlias.objects.get(name='speaker_2_last_name')
FIELD_ALIAS_SPEAKER_2_UNIVERSITY = CustomFieldAlias.objects.get(name='speaker_2_university')
FIELD_ALIAS_TEAM = CustomFieldAlias.objects.get(name='team_name')

CUSTOM_FIELD_SETS = [
    (FIELD_ALIAS_TEAM, LBL_CUSTOM_FIELD_TEAM, True),

    (FIELD_ALIAS_SPEAKER_1, LBL_CUSTOM_FIELD_SPEAKER_1_EMAIL, True),
    (FIELD_ALIAS_SPEAKER_1_F_NAME, LBL_CUSTOM_FIELD_SPEAKER_1_F_NAME, False),
    (FIELD_ALIAS_SPEAKER_1_L_NAME, LBL_CUSTOM_FIELD_SPEAKER_1_L_NAME, False),

    (FIELD_ALIAS_SPEAKER_2, LBL_CUSTOM_FIELD_SPEAKER_2_EMAIL, True),
    (FIELD_ALIAS_SPEAKER_2_F_NAME, LBL_CUSTOM_FIELD_SPEAKER_2_F_NAME, False),
    (FIELD_ALIAS_SPEAKER_2_L_NAME, LBL_CUSTOM_FIELD_SPEAKER_2_L_NAME, False),
]

REQUIRED_ALIASES = [FIELD_ALIAS_SPEAKER_1, FIELD_ALIAS_SPEAKER_2, FIELD_ALIAS_TEAM]
