import os

DEBUG = os.getenv('DJANGO_DEBUG', 'OFF') == 'ON'
DEBUG_TOOLBAR = os.getenv('DJANGO_DEBUG_TOOLBAR', 'OFF') == 'ON'

if DEBUG_TOOLBAR:
    from . defaults import INSTALLED_APPS, MIDDLEWARE

    INSTALLED_APPS += [
        'debug_toolbar',
        'template_timings_panel',
    ]

    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

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

    DEBUG_TOOLBAR_CONFIG = {
        'JQUERY_URL': 'https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js',
        'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
    }
