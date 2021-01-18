import django_tables2 as tables
from django_tables2.utils import A
from .models import (
    Pollingstation, District, County, Subcounty, Parish, ElectionCandidate
)


class BaseMetaClass:
    abstract = True
    attrs = {"class": "table table-striped table-responsive table-bordered"}

    
class PollingStationTable(tables.Table):
    name  = tables.LinkColumn("pollingstation-detail", text=lambda record: record.name, args=[A("pk")])
    class Meta(BaseMetaClass):
        model = Pollingstation
        fields = ['id', 'name', 'code', 'county', 'total_voters']


class DistrictTable(tables.Table):
    name  = tables.LinkColumn("district-detail", text=lambda record: record.name, args=[A("pk")])
    
    class Meta(BaseMetaClass):
        model = District
        fields = ['name', ]
    

class CountyTable(tables.Table):
    name  = tables.LinkColumn("county-detail", text=lambda record: record.name, args=[A("pk")])
    class Meta(BaseMetaClass):
        model = County
        fields = ['name', 'district']


class SubcountyTable(tables.Table):
    name  = tables.LinkColumn("subcounty-detail", text=lambda record: record.name, args=[A("pk")])
    class Meta(BaseMetaClass):
        model = Subcounty
        fields = ['name', 'county']


class ParishTable(tables.Table):
    name  = tables.LinkColumn("parish-detail", text=lambda record: record.name, args=[A("pk")])
    class Meta(BaseMetaClass):
        model = Parish
        fields = ['name', 'subcounty']


class ElectionCandidateTable(tables.Table):
   
    class Meta(BaseMetaClass):
        model = ElectionCandidate
        fields = ['name', 'category', 'county', 'district', 'party', 'symbol']
