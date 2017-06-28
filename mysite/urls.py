"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from water import views

urlpatterns = [
    url(r'^water/', include('water.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^water/search/$', views.search, name='search'),
    url(r'^water/results/', views.results, name='results'),
    url(r'^WI(?P<source_id>[0-9]+)/ViolationTable/$', views.ViolationTable, name='Violation Table'),
    url(r'^WI(?P<source_id>[0-9]+)/$', views.details, name='details'),

]
