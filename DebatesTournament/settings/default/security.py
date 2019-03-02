# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '<SECRET_KEY>'  # Set random line

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DEBUG_TOOLBAR = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']

ADMINS = (('<name_1>', '<email_1>'), ('<name_2>', '<email_2>'),)

MANAGERS = (('<name_1>', '<email_1>'), ('<name_2>', '<email_2>'),)

if DEBUG:
    from ..default import INSTALLED_APPS, MIDDLEWARE

    INSTALLED_APPS += [
        'debug_toolbar',
        # 'template_timings_panel',
        # 'debug_toolbar_line_profiler',
    ]

    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

    INTERNAL_IPS = ['127.0.0.1']

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]
