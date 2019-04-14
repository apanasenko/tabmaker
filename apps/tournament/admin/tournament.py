from django.contrib.admin import ModelAdmin
from apps.tournament.models import Tournament


class TournamentAdmin(ModelAdmin):

    list_display = [
        'id',
        'name',
        'location_sub',
        'owner',
        'start_tour',
        'status',
        'cur_round',
        'teams_count',
        'adjudicators_count',
    ]


    def owner(self, tournament: Tournament):
        from apps.tournament import consts
        return tournament.get_users([consts.ROLE_OWNER])[0].user.id


    def teams_count(self, tournament: Tournament):
        return tournament.get_teams().count()


    def adjudicators_count(self, tournament: Tournament):
        from apps.tournament import consts
        return tournament.get_users(consts.ADJUDICATOR_ROLES).count()


    def location_sub(self, tournament: Tournament) -> str:
        return ', '.join(tournament.location.split(',')[:3])

    location_sub.admin_order_field = 'location'
