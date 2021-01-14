from voting.views.web import (
    DistrictListView, DistrictDetailView,
    CountyListView, CountyDetailView,
    SubcountyListView, SubcountyDetailView,
    ParishListView, ParishDetailView, DashboardView,
    PollingstationListView, PollingstationDetailView,
    PollingCandidatesDataUploadView, PollingStationDataUploadView,
    show_all_candidates
)
from django.urls import path

urlpatterns = [
    path('', DashboardView.as_view(), name="dashboard"),
    path('district', DistrictListView.as_view(), name="district-list"),
    path('district/<int:pk>/detail', DistrictDetailView.as_view(), name="district-detail"),
    path('county', CountyListView.as_view(), name="county-list"),
    path('country/<int:pk>/detail', CountyDetailView.as_view(), name="county-detail"),
    path('subcounty', SubcountyListView.as_view(), name="subcounty-list"),
    path('subcounty/<int:pk>/detail', SubcountyDetailView.as_view(), name="subcounty-detail"),
    path('parish', ParishListView.as_view(), name="parish-list"),
    path('parish/<int:pk>/detail', ParishDetailView.as_view(), name="parish-detail"),
    path('pollingstation', PollingstationListView.as_view(), name="pollingstation-list"),
    path('pollingstation/<int:pk>/detail', PollingstationDetailView.as_view(), name="pollingstation-detail"),
    path('pollingstation-dataupload', PollingStationDataUploadView.as_view(), name="pollingstation-dataupload"),
    path('pollingcandidate-dataupload', PollingCandidatesDataUploadView.as_view(), name="pollingcandidate-dataupload"),
    path('candidates', show_all_candidates, name="all-candidates")
]
