
import os
import csv
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django_tables2 import RequestConfig
from water.tables import Effluent_Data_Table, Location_Table
from water.models import MyCSvModel, MyCSvModel2, Location_Data
from geopy.distance import distance as geopy_distance
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

violator_file = '/Users/barry_b_esq/Google Drive/PollutionWatch/webmaterials/EPAWaterViolators.csv'
violator_csv_list = MyCSvModel.import_data(data=open(violator_file))
eff_viols_file = '/Users/barry_b_esq/Google Drive/PollutionWatch/webmaterials/WI_NPDES_EFF_VIOLATIONS.csv'
eff_viols_csv_list = MyCSvModel2.import_data(data=open(eff_viols_file))

def index(request):
    violator_list_ctime = os.path.getctime(violator_file)
    violator_list_created_date = datetime.fromtimestamp(violator_list_ctime).strftime('%A, %B %d, %Y')
    return render(request, 'index.html', {'violator_list': violator_csv_list, 'violator_list_created_date': violator_list_created_date})

def details(request, source_id):
    for permittee in violator_csv_list:
        if source_id in permittee.source_id:
            geolocator = Nominatim()
            download_file_loc = ("https://ofmpub.epa.gov/echo/eff_rest_services.download_effluent_chart?p_id=" + permittee.source_id + "&start_date=01/01/2013&end_date=03/31/2016")
            permittee.latitude = str(permittee.fac_lat)
            permittee.longitude = str(permittee.fac_long)
            search_address = (permittee.cwp_street + ", " + permittee.cwp_city + ", " + permittee.cwp_state)
            location = permittee.latitude, permittee.longitude
            static_map = ("https://maps.google.com/maps/api/staticmap?zoom=11&size=450x450&sensor=false&markers=color:blue%7C"+permittee.latitude+','+permittee.longitude)
            try:
                return render(request, 'details.html',
                                  {'permittee': permittee, 'address': search_address, 'location': location,
                                    'download_file_loc': download_file_loc, 'static_map': static_map})
            except GeocoderTimedOut:
                return render(request, 'details.html',
                                  {'permittee': permittee, 'address': search_address, 'location': location,
                                    'download_file_loc': download_file_loc})
                #HttpResponse ("Geocoder Timed Out. Please Try Again.")
                #return render(request, 'details-nomap.html', {'permittee': permittee, 'address': search_address, 'compliance_dict': compliance_dict, 'snc_code': snc_code, 'download_file_loc': download_file_loc})

def EffluentData (request, source_id):
    file_name = ('/Users/barry_b_esq/Google Drive/PollutionWatch/EPAData/WI' + source_id + '-formatted.csv')
    effluent_csv_list = MyCSvModel2.import_data(data=open(file_name))
    effluent_list_ctime = os.path.getctime(file_name)
    effluent_list_created_date = datetime.fromtimestamp(effluent_list_ctime).strftime('%A, %B %d, %Y')
    for permittee in violator_csv_list:
        if source_id in permittee.source_id:
            return render(request, 'EffluentData.html', {'violator_list': violator_csv_list, 'permittee': permittee, 'effluent_list': effluent_csv_list, 'effluent_list_created_date': effluent_list_created_date})

def violations(request, source_id):
    violator_csv_list = MyCSvModel.import_data(data=open(violator_list))
    file_name = ('/Users/barry_b_esq/Google Drive/PollutionWatch/EPAData/WI' + source_id + '-formatted.csv')
    effluent_csv_list = MyCSvModel2.import_data(data=open(file_name))
    effluent_list_ctime = os.path.getctime(file_name)
    effluent_list_created_date = datetime.fromtimestamp(effluent_list_ctime).strftime('%A, %B %d, %Y')
    effluent_list = []
    for permittee in violator_csv_list:
        if source_id in permittee.source_id:
            for item in effluent_csv_list:
                if item.violation_severity > 0:
                    effluent_list.append(item)
            return render(request, 'violations.html', {'permittee': permittee, 'effluent_list': effluent_list, 'effluent_list_created_date': effluent_list_created_date})

def ViolationTable(request, source_id):
#    effluent_list_ctime = os.path.getctime(eff_viols_csv)
#    effluent_list_created_date = datetime.fromtimestamp(effluent_list_ctime).strftime('%A, %B %d, %Y')
    indiv_effluent_list = []
    count = 0
    for permittee in violator_csv_list:
        if source_id in permittee.source_id:
            for violation in eff_viols_csv_list:
                if source_id in violation.npdes_id:
                    indiv_effluent_list.append(violation)
                    count = count + 1
            table = Effluent_Data_Table(indiv_effluent_list)
            table.paginate(page=request.GET.get('page', 1), per_page=25)
            if count > 0:
                return render(request, 'ViolationTable.html', {'table': table, 'permittee': permittee})
            else:
                return HttpResponse('No effluent data available')

def search(request):
    return render(request, 'search.html')

def results(request):
    if 'q' in request.GET and request.GET['q']:
        try:
            q = request.GET['q']
            geolocator = Nominatim()
            qhome = geolocator.geocode(q)
            qhome_coords = (qhome.latitude, qhome.longitude)
            count = 0
            location_list = Location_Data
            location_list.objects.all().delete()
            for permittee in violator_csv_list:
                location_coords = (permittee.fac_lat, permittee.fac_long)
                if permittee.fac_lat > 0:
                    d_qhome = geopy_distance(qhome_coords, location_coords)
                    item = location_list(cwp_name = permittee.cwp_name, fac_lat = permittee.fac_lat, fac_long = permittee.fac_long, d_qhome = d_qhome.mi)
                    item.save()
                    count=count+1
                else:
                    pass
        except GeocoderTimedOut:
            return HttpResponse('GeoCoder Timed Out. Please try again.')
        if location_list is "":
            return HttpResponse('No search results. Please try again.')
        else:
            table = Location_Table(location_list.objects.all())
            RequestConfig(request).configure(table)
            return render(request, 'search_results.html', {'table': table, 'qhome': qhome, 'query': q})
    else:
        return HttpResponse('Search error. Please try again.')