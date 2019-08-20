"""KETEP_DEV URL Configuration

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
from KETEP_DEV import views
from django.views.generic import TemplateView
from energy import views as ev

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^dashboard$', TemplateView.as_view(template_name="dashboard.html"), name='dashboard'),
    url(r'^query$', TemplateView.as_view(template_name="energy_query.html"), name='query'),
    url(r'^analysis$', TemplateView.as_view(template_name="energy_analysis.html"), name='analysis'),
    url(r'^control$', TemplateView.as_view(template_name="system_control.html"), name='control'),
    url(r'^target$', TemplateView.as_view(template_name="target_management.html"), name='target'),
    url(r'^room$', TemplateView.as_view(template_name="room_management.html"), name='room'),
    url(r'^sAdmin$', TemplateView.as_view(template_name="super_admin.html"), name='sAdmin'),
    url(r'^getWeatherInfo/$', views.getWeatherInfo, name='getWeatherInfo'),
    url(r'^getIsmartData/$', views.getIsmartData, name='getIsmartData'),
    url(r'^getUsage/$', ev.getUsage, name='getUsage'),
    url(r'^testgame/$', TemplateView.as_view(template_name="energy_analysis.html"), name='testgame'),
]
