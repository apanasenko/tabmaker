from django.core.management.base import BaseCommand
from apps.tournament.utils import detect_motion_language

from apps.tournament.models import Motion


class Command(BaseCommand):
    #
    def add_arguments(self, parser):
        parser.add_argument('id', type=int)

    def handle(self, *args, **options):
        print(options['id'])

        motions = Motion.objects.filter(id=options['id']) if options['id'] > 0 \
            else Motion.objects.filter(is_public=True, language=None).order_by('-id')

        for motion in motions:
            print(motion.id)
            print(motion.motion)
            print(motion.infoslide)

            if not detect_motion_language(motion):
                    return

            print(motion.language.name)
            print('')
            print('')
            print('')
