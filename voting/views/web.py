from voting.models import (
    District, County, Subcounty, Parish, Pollingstation
)
from django.views.generic import ListView, DetailView, View
from voting.forms import (
    PollingStationDataUploadForm, PollingCandidateDataUploadForm
)
from django.shortcuts import render, redirect
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


class DistrictListView(ListView):
    model = District
    template_name = 'voting/districts/all.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Districts'
        return context


class DistrictDetailView(DetailView):
    model = District
    template_name = 'voting/districts/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'District Details'
        return context


class CountyListView(ListView):
    model = County
    template_name = 'voting/counties/all.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Counties'
        return context


class CountyDetailView(DetailView):
    model = County
    template_name = 'voting/counties/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'County Details'
        return context


class SubcountyListView(ListView):
    model = Subcounty
    template_name = 'voting/sub-counties/all.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Sub Counties'
        return context


class SubcountyDetailView(DetailView):
    model = Subcounty
    template_name = 'voting/sub-counties/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Subcounty Details'
        return context


class ParishListView(ListView):
    model = Parish
    template_name = 'voting/parishes/all.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Parishes'
        return context


class ParishDetailView(DetailView):
    model = Parish
    template_name = 'voting/parishes/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Parish Details'
        return context


class PollingstationListView(ListView):
    model = Pollingstation
    template_name = 'voting/polling-stations/all.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Polling Stations'
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
        print(request)
        try:
            file = request.FILES['file']
            if (str(file).split('.')[-1] == "xls"):
                data = xls_get(file, column_limit=12)
            elif (str(file).split('.')[-1] == "xlsx"):
                data = xlsx_get(file, column_limit=12)
            else:
                return redirect('/pollingstations')

            # The data is in a sheet labelled PS
            # ToDo: We'll refactor this later. For now, I need to get the data into the application
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
            return redirect('/pollingstations')
        except MultiValueDictKeyError:
            print('Exception caught')
            return redirect('/pollingstations')


class PollingCandidatesDataUploadView(View):
    def get(self, request):
        form = PollingCandidateDataUploadForm()
        context = {'form': form, 'page_title': 'Upload Candidate Data'}
        return render(request, 'voting/polling-candidate-upload.html', context)

    def post(self, request):
        pass


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'voting/dashboard')


def show_all_candidates(request):
    context = {'page_title': 'All Candidates'}
    return render(request, 'voting/candidates.html', context)
