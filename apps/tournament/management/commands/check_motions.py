from django.core.management.base import BaseCommand

from apps.tournament.models import Motion


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('id', nargs='+', type=int)

    def handle(self, *args, **options):
        print(options['id'])
        for i in Motion.objects.filter(id__gte=options['id'][0]):
            print(i.id)
            print(i.motion)
            print(i.infoslide)
            i.is_public = int(input())
            i.save()
