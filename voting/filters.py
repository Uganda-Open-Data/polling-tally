import django_filters
from voting.models import Pollingstation, District, County, Subcounty, Parish
from django_filters import CharFilter

class BaseFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
class PollingStationFilter(BaseFilter):
    class Meta:
        model = Pollingstation
        fields = ['name', 'county', 'total_voters']


class DistrictFilter(BaseFilter):
    
    class Meta:
        model = District
        fields = ['name']


class CountyFilter(BaseFilter):
    class Meta:
        model = County
        fields = ['name', 'district']


class SubcountyFilter(BaseFilter):
    class Meta:
        model = Subcounty
        fields = ['name', 'county']


class ParishFilter(BaseFilter):
    class Meta:
        model = Parish
        fields = ['name', 'subcounty']
