import django_tables2 as tables
from .models import Pollingstation, District, County, Subcounty, Parish


class BaseMetaClass:
    abstract = True
    attrs = {"class": "table table-striped table-responsive table-bordered"}


class PollingStationTable(tables.Table):
    class Meta(BaseMetaClass):
        model = Pollingstation
        fields = ['id', 'name', 'code', 'county', 'total_voters']


class DistrictTable(tables.Table):
    class Meta(BaseMetaClass):
        model = District
        fields = ['name']


class CountyTable(tables.Table):
    class Meta(BaseMetaClass):
        model = County
        fields = ['name', 'district']


class SubcountyTable(tables.Table):
    class Meta(BaseMetaClass):
        model = Subcounty
        fields = ['name', 'county']


class ParishTable(tables.Table):
    class Meta(BaseMetaClass):
        model = Parish
        fields = ['name', 'subcounty']
