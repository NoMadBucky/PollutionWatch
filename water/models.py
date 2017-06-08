from django.db import models
from django import forms
from datetime import date
from adaptor.model import CsvModel, CsvDbModel
from adaptor.fields import CharField, IntegerField, DecimalField

class Permittees(models.Model):
    map_num = models.CharField(max_length = 2, default = '00')
    source_id = models.CharField(max_length = 30)
    registry_id = models.CharField(max_length = 36)
    cwp_name = models.CharField(max_length = 80)
    cwp_street = models.CharField(max_length = 100, default = 'DEFAULT VALUE')
    cwp_city = models.CharField(max_length = 60, default = 'DEFAULT VALUE')
    cwp_state = models.CharField(max_length = 2, default = 'NA')
    cwp_facility_type_indicator = models.CharField(max_length = 10, default = '')
    cwp_major_minor = models.CharField(max_length = 1, default='0')
    cwp_qtrs_in_nc = models.CharField(max_length = 5, default = 'N/A')
    cwp_current_viol = models.CharField(max_length = 5, default='N/A')
    fac_lat = models.DecimalField(decimal_places = 6, max_digits = 8, default = 0.000000)
    fac_long = models.DecimalField(decimal_places = 6, max_digits = 8, default = 0.000000)
    cwp_e90 = models.CharField(max_length = 22, default = 'N/A')
    cwp_formal_ea = models.CharField(max_length = 5, default = 'N/A')
    cwp_days_last_inspection = models.CharField(max_length = 5, default = 'N/A')
    poll_in_violation = models.CharField(max_length = 300, default = 'NONE')
    def __str__(self):
        return 'Name: %s, WPDES: %s, Reg_ID: %s' % (self.cwp_name, self.source_id, self.registry_id)

class MyCSvModel(CsvDbModel):
    class Meta:
        delimiter = ','
        has_header = False
        dbModel = Permittees

class Effluent_Data(models.Model):
    npdes_id = models.CharField(max_length = 9, default = 'NA', verbose_name='Permit Number')
    version_nmbr = models.IntegerField(null=True)
    activity_id = models.IntegerField(default=0)
    npdes_violation_id = models.IntegerField(default=0, verbose_name='Violation Number')
    perm_feature_nmbr = models.CharField(max_length=4, default='NA')
    permit_activity_id = models.IntegerField(default=0)
    dmr_form_value_id = models.IntegerField(default=0)
    dmr_value_nmbr = models.FloatField(default = 0, verbose_name='DMR Value')
    dmr_value_id = models.IntegerField(default=0, null = True)
    dmr_parameter_id = models.IntegerField(default=0, null=True)
    nodi_code = models.CharField(max_length=3, blank=True)
    adjusted_dmr_value_nmbr = models.DecimalField(max_digits = 22, decimal_places=5, null=True)
    violation_type_code = models.CharField(max_length=6, blank=True)
    violation_type_desc = models.CharField(max_length=100, blank=True)
    violation_code = models.CharField(max_length=5, default='NA', verbose_name='Violation Code')
    violation_desc = models.CharField(max_length=100, default='NA', verbose_name='Violation Description')
    parameter_code = models.CharField(max_length=5, default='NA')
    parameter_desc = models.CharField(max_length=100, default='NA', verbose_name='Parameter Description')
    monitoring_period_end_date = models.DateField(blank=True, null=True)
    exceedance_pct = models.FloatField(default=0, null=True)
    value_qualifier_code = models.CharField(max_length=3, blank=True)
    unit_code = models.CharField(max_length=2, blank=True)
    value_received_date = models.DateField(null=True, blank=True, verbose_name='Date Reported')
    days_late = models.FloatField(default=0, null=True, verbose_name='Days Late')
    adjusted_dmr_standard_units = models.DecimalField(max_digits=22, decimal_places=5, null=True)
    limit_id = models.FloatField(default=0)
    dmr_value_standard_units = models.FloatField(default=0, null=True)
    value_type_code = models.CharField(max_length=3, default='NA')
    rnc_detection_code = models.CharField(max_length=3, blank=True)
    rnc_detection_desc = models.CharField(max_length=100, blank=True, verbose_name='Noncompliance Description')
    rnc_detection_date = models.DateField(blank=True, null=True)
    rnc_resolution_code = models.CharField(max_length=3, blank=True)
    rnc_resolution_desc = models.CharField(max_length=100, blank=True)
    rnc_resolution_date = models.DateField(blank=True, null=True)
    statistical_base_code = models.CharField(max_length=3, default='NA')
    statistical_base_monthly_avg = models.CharField(max_length=1, blank=True)

class MyCSvModel2(CsvDbModel):
    class Meta:
        delimiter = ','
        has_header = True
        dbModel = Effluent_Data

class Location_Data(models.Model):
    cwp_name = models.CharField(max_length = 150)
    fac_lat = models.DecimalField(decimal_places=4, max_digits=6, default= 0.0000)
    fac_long = models.DecimalField(decimal_places=4, max_digits=6, default= 0.0000)
    d_qhome = models.FloatField(default = 0.0)