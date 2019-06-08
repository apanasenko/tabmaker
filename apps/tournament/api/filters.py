from django_filters import rest_framework as filters


class AdjudicatorConflictFilter(filters.FilterSet):
    tournament = filters.NumberFilter()
