from django.db.utils import OperationalError
from water.models import Effluent_Data


eff_viols_csv_file = 'WI_NPDES_EFF_VIOLATIONS.csv'
eff_viols_csv_list = []
f = open(eff_viols_csv_file, 'r')
try:
    for line in f:
        line = line.split(';')
        tmp = Effluent_Data.objects.create(npdes_id = line[0])
        eff_viols_csv_list.append(tmp)
    f.close()
except OperationalError:
    pass