import os
from urllib.parse import urlparse

BASE_DIR = os.getenv('DJANGO_BASE_DIR', os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',

    'analytics',
    'apps.tester',
    'apps.tournament',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.mailru',
    'allauth.socialaccount.providers.vk',
    'allauth.socialaccount.providers.facebook',

    'modeltranslation',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                # 'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'apps.tournament.utils.debug_mode',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'
            ],
        },
    },
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
]

ROOT_URLCONF = 'DebatesTournament.urls'

WSGI_APPLICATION = 'DebatesTournament.wsgi.application'

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Asia/Vladivostok'

USE_I18N = True

USE_L10N = True

LANGUAGES = (
    ('ru', 'Russian'),
    ('en', 'English'),
)

MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'

AUTH_USER_MODEL = 'tournament.User'

WEBPACK_DEV_SERVER = os.getenv('WEBPACK_DEV_SERVER', None)

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'secret')

ALLOWED_HOSTS = [urlparse(os.getenv('MAIN_SITE')).hostname]

# TODO подумать, может можно лучше
ADMINS = [
    (os.getenv('DJANGO_ADMIN_NAME_' + str(i), ''), os.getenv('DJANGO_ADMIN_EMAIL_' + str(i), ''))
    for i in range(1, int(os.getenv('DJANGO_ADMINS_COUNT', 0)))
]

MANAGERS = [
    (os.getenv('DJANGO_MANAGER_NAME_' + str(i), ''), os.getenv('DJANGO_MANAGER_EMAIL_' + str(i), ''))
    for i in range(1, int(os.getenv('DJANGO_MANAGERS_COUNT', 0)))
]

YANDEX_VERIFICATION = os.getenv('YANDEX_VERIFICATION', 0)
GOOGLE_VERIFICATION = os.getenv('GOOGLE_VERIFICATION', 0)
NEVER_BOUNCE_KEY = os.getenv('NEVER_BOUNCE_KEY', 0)
