from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^WI(?P<source_id>[0-9]+)/$', views.details, name='details'),
    url(r'^WI(?P<source_id>[0-9]+)/ViolationTable/$', views.ViolationTable, name='Violation Table'),
]