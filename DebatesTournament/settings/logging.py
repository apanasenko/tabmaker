from . import BASE_DIR
import os

if os.getenv('DJANGO_LOG', 'OFF') == 'ON':
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': os.getenv('DJANGO_LOG_FILE', os.path.join(BASE_DIR, 'django.log')),
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
            'TelegramBot': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        },
    }
