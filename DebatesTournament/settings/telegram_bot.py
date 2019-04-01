from . defaults import INSTALLED_APPS
import os

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', None)

if TELEGRAM_BOT_TOKEN:
    INSTALLED_APPS += [
        'django_telegrambot',
    ]

    DJANGO_TELEGRAMBOT = {
        'MODE': os.getenv('TELEGRAM_BOT_MODE', 'POLLING'),
        'WEBHOOK_SITE': os.getenv('MAIN_SITE', ''),
        'WEBHOOK_PREFIX': '/telegram',
        'STRICT_INIT': True,
        'BOTS': [
            {
                'TOKEN': TELEGRAM_BOT_TOKEN,
            },
        ],
        'ALLOWED_UPDATES': ["callback_query"],
    }
