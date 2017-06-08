from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^results/', views.results, name='results'),
    url(r'^WI(?P<source_id>[0-9]+)/$', views.details, name='details'),
    url(r'^WI(?P<source_id>[0-9]+)/EffluentData/$', views.EffluentData, name='Effluent Data'),
    url(r'^WI(?P<source_id>[0-9]+)/violations/$', views.violations, name='violations'),
    url(r'^WI(?P<source_id>[0-9]+)/ViolationTable/$', views.ViolationTable, name='Violation Table'),
]