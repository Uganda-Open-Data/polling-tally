from voting.views.web import (
    DistrictListView, DistrictDetailView,
    CountyListView, CountyDetailView,
    SubcountyListView, SubcountyDetailView,
    ParishListView, ParishDetailView,
    PollingstationListView, PollingstationDetailView
)
from django.urls import path

urlpatterns = [
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
]
