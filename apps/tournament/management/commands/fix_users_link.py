from django.core.management.base import BaseCommand
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from apps.tournament.models import User
import re


class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        validator = URLValidator()
        for user in User.objects.all():
            try:
                l1 = user.link
                if user.link == '':
                    continue
                elif user.link.find('vk.com') > -1:
                    user.link = re.sub('^.{0,10}vk\.com', 'https://vk.com', user.link)
                    if l1 != user.link:
                        self.stdout.write(self.style.SUCCESS('VK %s -> %s' % (l1, user.link)))
                elif re.search('id\d+$', user.link) is not None:
                    user.link = re.sub('^.*?(id\d+)', r'https://vk.com/\1', user.link)
                    if l1 != user.link:
                        self.stdout.write(self.style.SUCCESS('ID %s -> %s' % (l1, user.link)))
                else:
                    # pass
                    validator(user.link)
            except ValidationError:
                self.stdout.write(self.style.ERROR('FAIL "%s"' % user.link))
                user.link = ''

            user.save()
