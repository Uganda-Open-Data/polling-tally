import django_tables2 as tables
from .models import Pollingstation, District


class PollingStationTable(tables.Table):
    class Meta:
        model = Pollingstation
        attrs = {"class": "table table-striped table-responsive"}
        fields = ['id', 'name', 'code', 'county', 'total_voters']
