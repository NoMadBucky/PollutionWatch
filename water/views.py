
import os
import csv
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django_tables2 import RequestConfig
from geopy.distance import distance as geopy_distance
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from water.tables import Effluent_Data_Table, Location_Table
from water.models import Permittees, Effluent_Data, Location_Data
from django.db.utils import OperationalError

violator_list = []
violator_file = 'EPAWaterViolators.csv'
eff_viols_list = []
eff_viols_file = 'WI_NPDES_EFF_VIOLATIONS.csv'

def getViolatorsList():
    if (len(violator_list) > 0):
        return violator_list

    f = None
    try:
        f = open(violator_file, 'r')
    except IOError:
        print("Working dir: " + os.path.dirname(os.path.realpath(__file__)))
        raise

    try:
        for line in f:
            line =  line.split(';')
            tmp = Permittees.objects.create(
                map_num = line[0],
                source_id = line[1],
                registry_id = line[2],
                cwp_name = line[3],
                cwp_street = line[4],
                cwp_city = line[5],
                cwp_state = line[6],
                cwp_facility_type_indicator = line[7],
                cwp_major_minor = line[8],
                cwp_qtrs_in_nc = line[9],
                cwp_current_viol = line[10],
                fac_lat = line[11],
                fac_long = line[12],
                cwp_e90 = line[13],
                cwp_formal_ea = line[14],
                cwp_days_last_inspection = line[15],
                poll_in_violation = line[16])
            violator_list.append(tmp)
        f.close()
    except OperationalError:
        pass

    return violator_list

def getEffViolsList():
    if (len(eff_viols_list) > 0):
        return eff_viols_list

    f = None
    try:
        f = open(eff_viols_file, 'r')
    except IOError:
        print("Working dir: " + os.path.dirname(os.path.realpath(__file__)))
        raise

    try:
        for line in f:
            line =  line.split(';')
            tmp = Effluent_Data.objects.create(
                npdes_id=line[0],
                version_nmbr = line[1],
                activity_id = line[2],
                npdes_violation_id = line[3],
                perm_feature_nmbr = line[4],
                permit_activity_id = line[5],
                dmr_form_value_id = line[6],
                dmr_value_nmbr = line[7],
                dmr_value_id = line[8],
                dmr_parameter_id = line[9],
                nodi_code = line[10],
                adjusted_dmr_value_nmbr = line[11],
                violation_type_code = line[12],
                violation_type_desc = line[13],
                violation_code = line[14],
                violation_desc = line[15],
                parameter_code = line[16],
                parameter_desc = line[17],
                monitoring_period_end_date = line[18],
                exceedance_pct = line[19],
                value_qualifier_code = line[20],
                unit_code = line[21],
                value_received_date = line[22],
                days_late = line[23],
                adjusted_dmr_standard_units = line[24],
                limit_id = line[25],
                dmr_value_standard_units = line[26],
                value_type_code = line[27],
                rnc_detection_code = line[28],
                rnc_detection_desc = line[29],
                rnc_detection_date = line[30],
                rnc_resolution_code = line[31],
                rnc_resolution_desc = line[32],
                rnc_resolution_date = line[33],
                statistical_base_code = line[34],
                statistical_base_monthly_avg = line[35])
            eff_viols_list.append(tmp)
        f.close()
    except OperationalError:
        pass

    return eff_viols_list

def index(request):
    violator_list_ctime = os.path.getctime(violator_file)
    violator_list_created_date = datetime.fromtimestamp(violator_list_ctime).strftime('%A, %B %d, %Y')
    return render(request, 'index.html', {'violator_list': getViolatorsList(), 'violator_list_created_date': violator_list_created_date})

def details(request, source_id):
    for permittee in getViolatorsList():
        if source_id in permittee.source_id:
            download_file_loc = ("https://ofmpub.epa.gov/echo/eff_rest_services.download_effluent_chart?p_id=" + permittee.source_id + "&start_date=01/01/2013&end_date=03/31/2016")
            permittee.latitude = str(permittee.fac_lat)
            permittee.longitude = str(permittee.fac_long)
            embed_map = ("https://google.com/maps/embed/v1/place?key=AIzaSyA2pjsCYUlRAYfm96meB9LmtdgbJUVatig&q=" + permittee.latitude + ',' + permittee.longitude + "&zoom=14&maptype=satellite")
            return render(request, 'details.html', {'permittee': permittee, 'download_file_loc': download_file_loc, 'embed_map': embed_map})

def ViolationTable(request, source_id):
    indiv_effluent_list = []
    for permittee in getViolatorsList():
            if source_id in permittee.source_id:
                name = permittee.cwp_name
    for violation in getEffViolsList():
        if source_id in violation.npdes_id:
            indiv_effluent_list.append(violation)

    if len(indiv_effluent_list) > 0:
        table = Effluent_Data_Table(indiv_effluent_list)
        table.paginate(page=request.GET.get('page', 1), per_page=25)
        return render(request, 'ViolationTable.html', {'table': table, 'permittee': name})
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
            for permittee in getViolatorsList():
                location_coords = (permittee.fac_lat, permittee.fac_long)
                d_qhome = geopy_distance(qhome_coords, location_coords)
                item = location_list(cwp_name = permittee.cwp_name, fac_lat = permittee.fac_lat, fac_long = permittee.fac_long, d_qhome = round(d_qhome.mi,1))
                item.save()
                count=count+1
        except GeocoderTimedOut:
            return HttpResponse('GeoCoder Timed Out. Please try again.')
        except GeocoderServiceError:
            return HttpResponse('GeoCoder Service Error. Please try again.')
        if location_list is "":
            return HttpResponse('No search results. Please try again.')
        else:
            table = Location_Table(location_list.objects.all())
            table.paginate(page=request.GET.get('page', 1), per_page=25)
            return render(request, 'search_results.html', {'table': table, 'qhome': qhome, 'query': q})
    else:
        return HttpResponse('Search error. Please try again.')