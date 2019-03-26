from django.core.management import BaseCommand

from analytics.models import MotionAnalysis
from apps.tournament.models import Motion, QualificationResult


def generate_analysis(motion):
    instance = MotionAnalysis()
    games = motion.game_set.all()
    for _ in games:
        for result in QualificationResult.objects.filter(game=_):
            try:
                instance.government_score += 8 - result.og - result.cg
                instance.opposition_score += 8 - result.oo - result.co
            except Exception:
                print(f'BUGGED {result.id}')

    instance.motion = motion
    instance.save()


class Command(BaseCommand):
    help = 'Generates motion statistics for specified motions'

    def add_arguments(self, parser):

        parser.add_argument(
            '--all',
            action='store_true',
            dest='all',
            help='Apply action for all motions',
        )

        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            help='Delete statistics for specified motions'
        )

    def handle(self, *args, **options):
        if options['all']:
            queryset = Motion.objects.all()
        else:
            queryset = Motion.objects.filter(pk__in=options['id'])
        for motion in queryset:
            if options['delete']:
                if motion.analysis:
                    motion.analysis.delete()
            else:
                generate_analysis(motion)
        return