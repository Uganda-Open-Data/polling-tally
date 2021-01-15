from django.contrib import admin
from voting.models import (
    District, County, Subcounty, Parish, Pollingstation, ElectionCandidates
)

# Register your models here.
appModels = [District, County, Subcounty, Parish, Pollingstation, ElectionCandidates]
admin.site.register(appModels)
