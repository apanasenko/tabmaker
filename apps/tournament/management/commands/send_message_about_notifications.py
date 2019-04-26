import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from apps.tournament.models import Tournament, TelegramToken
from django_telegrambot.apps import DjangoTelegramBot


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('tournament_id', type=int)

    def handle(self, *args, **options):
        tournament = Tournament.objects.get(pk=options['tournament_id'])
        bot_name = DjangoTelegramBot.getBot().username

        for team in tournament.get_teams():
            for speaker in team.team.get_speakers():

                if speaker.telegram_id:
                    continue

                html_content = render_to_string(
                    'tournament/start_tournament_email.html',
                    {
                        'tournament': tournament,
                        'bot_name': bot_name,
                        'token': TelegramToken.generate(speaker).value,
                    }
                )

                text_content = strip_tags(html_content)
                logging.info(html_content)
                logging.info(text_content)
                msg = EmailMultiAlternatives(tournament.name, text_content, settings.EMAIL_HOST_USER, [speaker.email])
                msg.attach_alternative(html_content, 'text/html')
                msg.send()
