"""KETEP_DashBoard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from KETEP_DashBoard import views
from django.views.generic import TemplateView
from energy import views as ev

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^dashboard$', TemplateView.as_view(template_name="dashboard.html"), name='dashboard'),
    url(r'^query$', TemplateView.as_view(template_name="energy_query.html"), name='query'),
    url(r'^analysis$', TemplateView.as_view(template_name="energy_analysis.html"), name='analysis'),
    url(r'^control$', TemplateView.as_view(template_name="control.html"), name='control'),
    # url(r'^control$', views.getRoomInfo, name='control'),
    url(r'^target$', TemplateView.as_view(template_name="target_management.html"), name='target'),
    # url(r'^room$', TemplateView.as_view(template_name="room_management.html"), name='room'),
    url(r'^room$', views.getRoomInfo, name='room'),
    url(r'^roomAvrTrend$', TemplateView.as_view(template_name="roomAvrTrend.html"), name='roomAvrTrend'),
    url(r'^ahuStatus$', TemplateView.as_view(template_name="ahuStatus.html"), name='ahuStatus'),
    url(r'^ahuConfig$', TemplateView.as_view(template_name="ahuConfig.html"), name='ahuConfig'),
    url(r'^ahuSetting$', TemplateView.as_view(template_name="ahuSetting.html"), name='ahuSetting'),
    url(r'^ahuAvrTrend$', TemplateView.as_view(template_name="ahuAvrTrend.html"), name='ahuAvrTrend'),
    url(r'^sAdmin$', TemplateView.as_view(template_name="super_admin.html"), name='sAdmin'),
    url(r'^scheduleEdit$', TemplateView.as_view(template_name="schedule.html"), name='scheduleEdit'),
    url(r'^realTime$', TemplateView.as_view(template_name="energy_realTime.html"), name='realTime'),
    url(r'^getWeatherInfo/$', views.getWeatherInfo, name='getWeatherInfo'),
    url(r'^getIsmartData/$', views.getIsmartData, name='getIsmartData'),
    url(r'^getUsage/$', ev.getUsage, name='getUsage'),
    url(r'^getRoomTrend/$', views.getRoomTrend, name='getRoomTrend'),
    url(r'^getAhuStatus/$', views.getAhuStatus, name='getAhuStatus'),
    url(r'^getAhuTrend/$', views.getAhuTrend, name='getAhuTrend'),
    url(r'^getRoomAvrTrend/$', views.getRoomAvrTrend, name='getRoomAvrTrend'),
    url(r'^getAhuAvrTrend/$', views.getAhuAvrTrend, name='getAhuAvrTrend'),
    url(r'^testgame/$', TemplateView.as_view(template_name="energy_analysis.html"), name='testgame'),
]
