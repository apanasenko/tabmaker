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

ROLE_OWNER = TournamentRole.objects.filter(role_en='Owner').first()
ROLE_ADMIN = TournamentRole.objects.filter(role_en='Admin').first()
ROLE_CHIEF_ADJUDICATOR = TournamentRole.objects.filter(role_en='Chief adjudicator').first()

ROLE_TEAM_REGISTERED = TournamentRole.objects.filter(role_en='Registered').first()
ROLE_IN_TAB = TournamentRole.objects.filter(role_en='In tab').first()
ROLE_WAIT_LIST = TournamentRole.objects.filter(role_en='Wait list').first()
ROLE_VERIFIED = TournamentRole.objects.filter(role_en='Verified').first()  # Участник подтвердил участие
ROLE_APPROVED = TournamentRole.objects.filter(role_en='Approved').first()  # Организатор подтвердил
ROLE_MEMBER = TournamentRole.objects.filter(role_en='Member').first()

ROLE_ADJUDICATOR_REGISTERED = TournamentRole.objects.filter(role_en='Registered adjudicator').first()
ROLE_ADJUDICATOR_APPROVED = TournamentRole.objects.filter(role_en='Approved adjudicator').first()
ROLE_WING = TournamentRole.objects.filter(role_en='Wing').first()
ROLE_CHAIR = TournamentRole.objects.filter(role_en='Chair').first()

STATUS_REGISTRATION = TournamentStatus.objects.filter(name_en='Registration open').first()
STATUS_PREPARATION = TournamentStatus.objects.filter(name_en='Registration closed').first()
STATUS_STARTED = TournamentStatus.objects.filter(name_en='Qualification').first()
STATUS_PLAYOFF = TournamentStatus.objects.filter(name_en='Playoff').first()
STATUS_FINISHED = TournamentStatus.objects.filter(name_en='Finished').first()

TEAM_ROLES_NAMES = [
    'Registered',
    # 'In tab',
    # 'Wait list',
    # 'Verified',
    # 'Approved',
    'Member',
]

ADJUDICATOR_ROLES_NAMES = [
    'Registered adjudicator',
    # 'Approved adjudicator',
    'Wing',
    'Chair',
]

TEAM_ROLES = TournamentRole.objects.filter(role_en__in=TEAM_ROLES_NAMES)
ADJUDICATOR_ROLES = TournamentRole.objects.filter(role_en__in=ADJUDICATOR_ROLES_NAMES)

FORM_REGISTRATION_TYPE = CustomFormType.objects.filter(name='teams').first()
FORM_FEEDBACK_TYPE = CustomFormType.objects.filter(name='feedback').first()
FORM_ADJUDICATOR_TYPE = CustomFormType.objects.filter(name='adjudicator').first()
# FORM_AUDIENCE_TYPE = CustomFormType.objects.filter(name='audience').first()

CUSTOM_FORM_TYPES = {
    'team': FORM_REGISTRATION_TYPE,
    'feedback': FORM_FEEDBACK_TYPE,
    'adjudicator': FORM_ADJUDICATOR_TYPE,
    # 'audience': FORM_AUDIENCE_TYPE,
}

CUSTOM_FORM_QUESTIONS_TITLES = {
    FORM_REGISTRATION_TYPE: TITLE_CUSTOM_FORM_QUESTIONS_FOR_TEAM,
    FORM_ADJUDICATOR_TYPE: TITLE_CUSTOM_FORM_QUESTIONS_FOR_ADJUDICATOR,
    FORM_FEEDBACK_TYPE: TITLE_CUSTOM_FORM_QUESTIONS_FOR_FEEDBACK,
}

CUSTOM_FORM_ANSWERS_TITLES = {
    FORM_REGISTRATION_TYPE: TITLE_CUSTOM_FORM_ANSWERS_FOR_TEAM,
    FORM_ADJUDICATOR_TYPE: TITLE_CUSTOM_FORM_ANSWERS_FOR_ADJUDICATOR,
    FORM_FEEDBACK_TYPE: TITLE_CUSTOM_FORM_ANSWERS_FOR_FEEDBACK,
}

FIELD_ALIAS_SPEAKER_1 = CustomFieldAlias.objects.filter(name='speaker_1_email').first()
# FIELD_ALIAS_SPEAKER_1_F_NAME = CustomFieldAlias.objects.filter(name='speaker_1_first_name').first()
# FIELD_ALIAS_SPEAKER_1_L_NAME = CustomFieldAlias.objects.filter(name='speaker_1_last_name').first()
# FIELD_ALIAS_SPEAKER_1_UNIVERSITY = CustomFieldAlias.objects.filter(name='speaker_1_university').first()
FIELD_ALIAS_SPEAKER_2 = CustomFieldAlias.objects.filter(name='speaker_2_email').first()
# FIELD_ALIAS_SPEAKER_2_F_NAME = CustomFieldAlias.objects.filter(name='speaker_2_first_name').first()
# FIELD_ALIAS_SPEAKER_2_L_NAME = CustomFieldAlias.objects.filter(name='speaker_2_last_name').first()
# FIELD_ALIAS_SPEAKER_2_UNIVERSITY = CustomFieldAlias.objects.filter(name='speaker_2_university').first()
FIELD_ALIAS_TEAM = CustomFieldAlias.objects.filter(name='team_name').first()

FIELD_ALIAS_ADJUDICATOR = CustomFieldAlias.objects.filter(name='adjudicator').first()

CUSTOM_FIELD_SETS = {
    FORM_REGISTRATION_TYPE: [
        (FIELD_ALIAS_TEAM, LBL_CUSTOM_FIELD_TEAM, True),
        (FIELD_ALIAS_SPEAKER_1, LBL_CUSTOM_FIELD_SPEAKER_1_EMAIL, True),
        (FIELD_ALIAS_SPEAKER_2, LBL_CUSTOM_FIELD_SPEAKER_2_EMAIL, True),
    ],
    FORM_ADJUDICATOR_TYPE: [
        (FIELD_ALIAS_ADJUDICATOR, LBL_CUSTOM_FIELD_ADJUDICATOR, True),
    ],
}

REQUIRED_ALIASES = [
    FIELD_ALIAS_SPEAKER_1,
    FIELD_ALIAS_SPEAKER_2,
    FIELD_ALIAS_TEAM,
    FIELD_ALIAS_ADJUDICATOR,
]

CUSTOM_FORM_AJAX_ACTIONS = {
    'edit_question': 'edit',
    'remove_question': 'remove',
    'up_question': 'up',
    'down_question': 'down',
}
