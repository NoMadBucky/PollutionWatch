import django_tables2 as tables
from water.models import Effluent_Data, Location_Data

class Effluent_Data_Table(tables.Table):
    class Meta:
        attrs = {"class": "paleblue", "width":"100%"}
        model = Effluent_Data
        fields = ('npdes_id', 'npdes_violation_id', 'dmr_value_nmbr', 'violation_code', 'violation_desc', 'parameter_desc', 'value_received_date', 'days_late', 'rnc_detection_desc')
        order_by = ('-value_received_date')


class Location_Table(tables.Table):
    class Meta:
        model = Location_Data
        fields = ('cwp_name', 'fac_lat', 'fac_long', 'd_qhome')
        order_by = ('d_qhome')