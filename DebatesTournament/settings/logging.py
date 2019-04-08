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
            'bot_log_file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'encoding': 'utf-8',
                'filename': os.getenv('TELEGRAM_BOT_LOG_FILE', os.path.join(BASE_DIR, 'logs', 'bot.log')),
                'formatter': 'verbose',
            },
            'mail_admins': {
                'class': 'django.utils.log.AdminEmailHandler',
                'level': 'ERROR',
                'include_html': True,
            },
            'django_log_file': {
                'class': 'logging.handlers.WatchedFileHandler',
                'encoding': 'utf-8',
                'filename': os.getenv('DJANGO_LOG_FILE', os.path.join(BASE_DIR, 'logs', 'django.log')),
                'level': 'DEBUG',
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'TelegramBot': {
                'handlers': ['bot_log_file'],
                'level': 'INFO',
            },
            '': {
                'handlers': ['django_log_file', 'mail_admins'],
                'level': 'INFO',
            },
        },
    }
