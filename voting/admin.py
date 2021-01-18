from django.contrib import admin
from voting.models import (
    District, County, Subcounty, Parish, Pollingstation, ElectionCandidate
)

# Register your models here.
appModels = [District, County, Subcounty, Parish, Pollingstation, ElectionCandidate]
admin.site.register(appModels)
