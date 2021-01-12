import django_filters
from voting.models import Pollingstation


class PollingStationFilter(django_filters.FilterSet):

    class Meta:
        model = Pollingstation
        fields = ['name', 'county', 'total_voters']
