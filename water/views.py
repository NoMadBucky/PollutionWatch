
import os
import csv
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from water.tables import Effluent_Data_Table
from water.models import Permittees
from django.db.utils import OperationalError
#from water.load_eff_viols import eff_viols_csv_list

violator_file = 'EPAWaterViolators.csv'
violator_list = []
f = open(violator_file, 'r')
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

def index(request):
    violator_list_ctime = os.path.getctime(violator_file)
    violator_list_created_date = datetime.fromtimestamp(violator_list_ctime).strftime('%A, %B %d, %Y')
    return render(request, 'index.html', {'violator_list': violator_list, 'violator_list_created_date': violator_list_created_date})

def details(request, source_id):
    for permittee in violator_list:
        if source_id in permittee.source_id:
            download_file_loc = ("https://ofmpub.epa.gov/echo/eff_rest_services.download_effluent_chart?p_id=" + permittee.source_id + "&start_date=01/01/2013&end_date=03/31/2016")
            permittee.latitude = str(permittee.fac_lat)
            permittee.longitude = str(permittee.fac_long)
            search_address = (permittee.cwp_street + ", " + permittee.cwp_city + ", " + permittee.cwp_state)
            location = permittee.latitude, permittee.longitude
            static_map = ("https://maps.google.com/maps/api/staticmap?zoom=11&size=450x450&sensor=false&markers=color:blue%7C"+permittee.latitude+','+permittee.longitude)
            return render(request, 'details.html',
                                  {'permittee': permittee, 'address': search_address, 'location': location,
                                    'download_file_loc': download_file_loc, 'static_map': static_map})

def ViolationTable(request, source_id):
    eff_viols_csv_list = []
    #eff_viols_csv_list = []
    indiv_effluent_list = []
    count = 0

    for permittee in violator_list:
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
