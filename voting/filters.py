import django_filters
from voting.models import Pollingstation, District, County, Subcounty, Parish


class PollingStationFilter(django_filters.FilterSet):
    class Meta:
        model = Pollingstation
        fields = ['name', 'county', 'total_voters']


class DistrictFilter(django_filters.FilterSet):
    class Meta:
        model = District
        fields = ['name', 'county']


class CountyFilter(django_filters.FilterSet):
    class Meta:
        model = County
        fields = ['name', 'district']


class SubcountyFilter(django_filters.FilterSet):
    class Meta:
        model = Subcounty
        fields = ['name', 'county']


class ParishFilter(django_filters.FilterSet):
    class Meta:
        model = Parish
        fields = ['name', 'subcounty']
