import django_filters
from django.contrib.postgres.search import SearchVector

from analytics.models import MotionAnalysis
from apps.tournament.models import Motion


class MotionAnalysisFilter(django_filters.FilterSet):
    searchQuery = django_filters.CharFilter(method="filter_search")

    # https://docs.djangoproject.com/en/2.0/ref/contrib/postgres/search/
    def filter_search(self, queryset, name, value):
        if value:
            return queryset.annotate(search=SearchVector('motion', 'infoslide')).filter(search=value)
        return queryset

    class Meta:
        model = Motion
        fields = '__all__'
