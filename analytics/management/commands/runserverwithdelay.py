"""
Start $compass watch, command when you do $python manage.py runserver

file: main/management/commands/runserver.py

Add ´main´ app to the last of the installed apps
"""

from time import sleep

from django.core.management import call_command
from django.core.management.commands.runserver import BaseRunserverCommand


class Command(BaseRunserverCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--sleep', default='0', dest='sleep',
                            help='Specifies the sleep time before starting django server.')

    def inner_run(self, *args, **options):
        sleep_time = int(options.get('sleep'))
        sleep(sleep_time)
        super().inner_run(*args, **options)
