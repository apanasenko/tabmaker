from django.contrib.admin import ModelAdmin, SimpleListFilter
from apps.tournament.models import Motion


class TournamentListFilter(SimpleListFilter):

    title = 'Турнирные'

    parameter_name = 'is_tournament'

    def lookups(self, request, model_admin):

        return (
            (1, 'Да'),
            (0, 'Нет'),
        )

    def queryset(self, request, queryset):

        if not self.value() is None:
            return queryset.filter(round__tournament__isnull=(self.value() == '0'))


class MotionAdmin(ModelAdmin):

    list_display = [
        'id',
        'is_public',
        'language',
        'tournament_name',
        'tournament_location',
        'round_number',
        'is_playoff',
        'motion',
        'infoslide'
    ]

    list_filter = [
        TournamentListFilter,
    ]

    ordering = ['-round__tournament_id', '-id']
    actions = ['published_motion']

    def tournament_name(self, motion: Motion) -> str:
        r = motion.round_set.first()
        return r.tournament.name if r else ''

    tournament_name.admin_order_field = 'round__tournament_id'


    def is_playoff(self, motion: Motion) -> bool:
        r = motion.round_set.first()
        return r.is_playoff if r else False

    is_playoff.admin_order_field = 'round__is_palyoff   '


    def round_number(self, motion: Motion) -> int:
        r = motion.round_set.first()
        return r.number if r else -1

    round_number.admin_order_field = 'round__number'

    def tournament_location(self, motion: Motion) -> str:
        r = motion.round_set.first()
        return r.tournament.location.split(',')[0] if r else ''

    def get_queryset(self, request):
        qs = super().get_queryset(request)\
            .select_related('language') \
            .prefetch_related('round_set', 'round_set__tournament') \
            .exclude(motion='temp') \

        return qs

    def published_motion(self, request, queryset):
        from apps.tournament.utils import detect_motion_language

        for motion in queryset.all():
            motion.is_public = True
            detect_motion_language(motion)

    published_motion.short_description = 'Добавить в Telegram'
