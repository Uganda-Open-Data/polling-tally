from django.db import models
from django.contrib.auth.models import User


class BaseTimeStampedModel(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_updated_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-id']
    

class BaseNameModel(BaseTimeStampedModel):
    name = models.CharField(max_length=256)
    
    class Meta:
        abstract = True
        ordering = ['-id']


class LocaleBaseModel(BaseNameModel):
    code = models.CharField(max_length=64, unique=False)
    boundary_data = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True


class District(LocaleBaseModel):

    def __str__(self):
        return self.name


class County(LocaleBaseModel):
    district = models.ForeignKey('District', on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ' IN ' + self.district.name + ' DISTRICT'


class Subcounty(LocaleBaseModel):
    county = models.ForeignKey('County', on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ' IN ' + self.county.name + ' IN ' + self.county.district.name + ' DISTRICT'


class Parish(LocaleBaseModel):
    subcounty = models.ForeignKey('Subcounty', on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ' IN ' + self.subcounty.name + ' IN ' + self.subcounty.county.name + ' IN ' + self.subcounty.county.district.name + ' DISTRICT'


class Pollingstation(BaseNameModel):
    county = models.ForeignKey('County', on_delete=models.CASCADE)
    code = models.CharField(max_length=64, null=True)
    total_voters = models.IntegerField(blank=False)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True),

    def __str__(self):
        return self.name + ' IN ' + self.county.name + ' - ' + self.county.district.name + ' DISTRICT'


class ElectionCandidate(BaseNameModel):
    district = models.ForeignKey('District', on_delete=models.CASCADE)
    county = models.ForeignKey('County', on_delete=models.CASCADE, null=True)
    party = models.CharField(max_length=32, null=True)
    symbol = models.CharField(max_length=32, null=True)
    status = models.CharField(max_length=32, null=True)
    category = models.CharField(max_length=32, null=True)

    def __str__(self):
        return self.name + ' FOR ' + self.category + ' - ' + self.district.name + ' DISTRICT'


class ElectionResult(BaseTimeStampedModel):
    district = models.ForeignKey('District', on_delete=models.CASCADE)
    county = models.ForeignKey('County', on_delete=models.CASCADE, null=True)
    polling_station = models.ForeignKey('Pollingstation', on_delete=models.CASCADE, null=False)
    category = models.CharField(max_length=32, null=False)
    candidate = models.ForeignKey('ElectionCandidate', on_delete=models.CASCADE, null=True)
    count = models.IntegerField(null=False)
