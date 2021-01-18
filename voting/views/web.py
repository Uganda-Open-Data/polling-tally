from voting.models import (
    District, County, Subcounty, Parish, Pollingstation, ElectionCandidate
)
from django.views.generic import DetailView, View
from voting.forms import (
    PollingStationDataUploadForm, PollingCandidateDataUploadForm
)
from django.shortcuts import render, redirect
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from voting.tables import (
    PollingStationTable, DistrictTable, CountyTable, SubcountyTable, ParishTable, ElectionCandidateTable
)
from django_tables2 import RequestConfig
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from voting.filters import (
    DistrictFilter, CountyFilter, SubcountyFilter,
    ParishFilter, PollingStationFilter, ElectionCandidateFilter
)
import pandas as pd
import numpy as np

class DistrictListView(SingleTableMixin, FilterView):
    model = District
    template_name = 'voting/districts/all.html'
    filterset_class = DistrictFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Districts'
        data = District.objects.all()
        d_filter = DistrictFilter(self.request.GET, queryset=data)
        data = DistrictTable(d_filter.qs)
        RequestConfig(self.request, paginate={"per_page": 18}).configure(data)
        context['table'] = data
        return context


class DistrictDetailView(DetailView):
    model = District
    template_name = 'voting/districts/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'District Details'
        return context


class CountyListView(SingleTableMixin, FilterView):
    model = County
    template_name = 'voting/counties/all.html'
    filterset_class = CountyFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Counties'
        data = County.objects.all()
        c_filter = CountyFilter(self.request.GET, queryset=data)
        data = CountyTable(c_filter.qs)
        RequestConfig(self.request, paginate={"per_page": 18}).configure(data)
        context['table'] = data
        return context


class CountyDetailView(DetailView):
    model = County
    template_name = 'voting/counties/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'County Details'
        return context


class SubcountyListView(SingleTableMixin, FilterView):
    model = Subcounty
    template_name = 'voting/sub-counties/all.html'
    filterset_class = SubcountyFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Sub Counties'
        data = Subcounty.objects.all()
        ps_filter = SubcountyFilter(self.request.GET, queryset=data)
        data = SubcountyTable(ps_filter.qs)
        RequestConfig(self.request, paginate={"per_page": 18}).configure(data)
        context['table'] = data
        return context


class SubcountyDetailView(DetailView):
    model = Subcounty
    template_name = 'voting/sub-counties/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Subcounty Details'
        return context


class ParishListView(SingleTableMixin, FilterView):
    model = Parish
    template_name = 'voting/parishes/all.html'
    filterset_class = ParishFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Parishes'
        data = Parish.objects.all()
        ps_filter = ParishFilter(self.request.GET, queryset=data)
        data = ParishTable(ps_filter.qs)
        RequestConfig(self.request, paginate={"per_page": 18}).configure(data)
        context['table'] = data
        return context


class ParishDetailView(DetailView):
    model = Parish
    template_name = 'voting/parishes/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Parish Details'
        return context


class PollingstationListView(SingleTableMixin, FilterView):
    model = Pollingstation
    template_name = 'voting/polling-stations/all.html'
    filterset_class = PollingStationFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Polling Stations'
        data = Pollingstation.objects.all()
        ps_filter = PollingStationFilter(self.request.GET, queryset=data)
        data = PollingStationTable(ps_filter.qs)
        RequestConfig(self.request, paginate={"per_page": 18}).configure(data)
        context['table'] = data
        return context


class PollingstationDetailView(DetailView):
    model = Pollingstation
    template_name = 'voting/polling-stations/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Polling Station Details'
        return context


class PollingStationDataUploadView(View):
    def get(self, request):
        form = PollingStationDataUploadForm()
        context = {'form': form, 'page_title': 'Upload Polling Station Data'}
        return render(request, 'voting/polling-station-dataupload.html', context)

    def post(self, request):
        try:
            file = request.FILES['file']
            if (str(file).split('.')[-1] == "xls"):
                data = xls_get(file, column_limit=12)
            elif (str(file).split('.')[-1] == "xlsx"):
                data = xlsx_get(file, column_limit=12)
            else:
                return redirect('/pollingstations')

            # The data is in a sheet labelled PS
            # ToDo:Refactor We'll refactor this later. For now, I need to get the data into the application
            # So this function might be a long with multiple ifs, but it'll be okay.
            admin_user = User.objects.get(pk=1)
            excel_data = data['PS']
            clean_data = excel_data[7:]

            for row in clean_data:
                if (len(clean_data) > 0):
                    serial_no, district_code, district_name, county_code, county_name, subcounty_code, subcounty_name, parish_code, parish_name, polling_station_code, polling_station_name, voter_count = row
                    # Save District
                    # ToDo - Exclude excel column titles
                    if District.objects.filter(name=district_name, code=district_code).exists():
                        district = District.objects.get(name=district_name, code=district_code)
                    else:
                        if district_name:
                            district = District.objects.create(name=district_name, code=district_code, created_by=admin_user, updated_by=admin_user)

                    # Save Counties
                    if County.objects.filter(name=county_name, code=county_code).exists():
                        county_ = County.objects.get(name=county_name, code=county_code)
                    else:
                        if county_name:
                            county_ = County.objects.create(name=county_name, code=county_code, district=district, created_by=admin_user, updated_by=admin_user)

                    # Save Sub counties
                    if Subcounty.objects.filter(name=subcounty_name, code=subcounty_code).exists():
                        subcounty = Subcounty.objects.get(name=subcounty_name, code=subcounty_code)
                    else:
                        if subcounty_name:
                            subcounty = Subcounty.objects.create(name=subcounty_name, code=subcounty_code, county=county_, created_by=admin_user, updated_by=admin_user)

                    # Save Parishes
                    if Parish.objects.filter(name=parish_name, code=parish_code).exists():
                        pass
                    else:
                        if parish_name and parish_name:
                            Parish.objects.create(name=parish_name, code=parish_code, subcounty=subcounty, created_by=admin_user, updated_by=admin_user)

                    if county_:
                        # Save Polling Stations
                        if Pollingstation.objects.filter(name=polling_station_name, code=polling_station_code, county=county_).exists():
                            pass
                        else:
                            if polling_station_name and polling_station_name:
                                Pollingstation.objects.create(name=polling_station_name, code=polling_station_code, county=county_, total_voters=voter_count, created_by=admin_user, updated_by=admin_user)
            return redirect('/pollingstation')
        except MultiValueDictKeyError:
            print('Exception caught')
            return redirect('/pollingstation')


class PollingCandidatesDataUploadView(View):
    def get(self, request):
        form = PollingCandidateDataUploadForm()
        context = {'form': form, 'page_title': 'Upload Candidate Data'}
        return render(request, 'voting/polling-candidate-upload.html', context)

    def post(self, request):
        try:
            file = request.FILES['file']
            file_data = file.read()
            excel_data = pd.read_excel(file_data, dtype=object)
            clean_data = excel_data.replace(np.NaN, '#')
            itera = 0
            admin_user = User.objects.get(pk=1)
            for row in clean_data.values:
                category, district_name, district_code, county_name, county_code, candidate_name, party, status, symbol = row
                if District.objects.filter(name=district_name, code=district_code).exists():
                    district_ = District.objects.get(name=district_name, code=district_code)
                    if County.objects.filter(name=county_name, code=county_code, district=district_).exists():
                        county_ = County.objects.get(name=county_name, code=county_code, district=district_)
                        if ElectionCandidate.objects.filter(name=candidate_name, category=category, district=district_, county=county_).exists():
                            pass
                        else:
                            ElectionCandidate.objects.create(name=candidate_name,category=category, party=party, symbol=symbol, status=status,district=district_, county=county_, created_by=admin_user, updated_by=admin_user)
                    else:
                        # District Woman MPs don't have specific counties
                        if ElectionCandidate.objects.filter(name=candidate_name, category=category, district=district_).exists():
                            pass
                        else:
                            ElectionCandidate.objects.create(name=candidate_name,category=category, party=party, symbol=symbol, status=status,district=district_, created_by=admin_user, updated_by=admin_user)
                else:
                    print('Failed to find district ' + district_name)
            return redirect('/candidates')
        except MultiValueDictKeyError:
            print('Exception caught')
            return redirect('/candidates')

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        total_districts = District.objects.all().count()
        total_counties = County.objects.all().count()
        total_polling_stations = Pollingstation.objects.all().count()
        total_candidates = ElectionCandidate.objects.all().count()
        context = {
            'total_districts': total_districts,
            'total_counties': total_counties,
            'total_candidates': total_candidates,
            'total_polling_stations': total_polling_stations
        }
        return render(request, 'voting/dashboard.html', context)


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'voting/dashboard')


def show_all_candidates(request):
    context = {'page_title': 'All Candidates'}
    return render(request, 'voting/candidates.html', context)

class CandidateListView(SingleTableMixin, FilterView):
    model = ElectionCandidate
    template_name = 'voting/candidates.html'
    filterset_class = ElectionCandidateFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'All Candidates'
        data = ElectionCandidate.objects.all()
        ps_filter = ElectionCandidateFilter(self.request.GET, queryset=data)
        data = ElectionCandidateTable(ps_filter.qs)
        RequestConfig(self.request, paginate={"per_page": 18}).configure(data)
        context['table'] = data
        return context