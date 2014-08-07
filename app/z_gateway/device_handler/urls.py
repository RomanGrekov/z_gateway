from django.conf.urls import patterns, url

from device_handler import views

urlpatterns = patterns('',
    url(r'^devices/all/$', views.devices, name='devices'),
    url(r'^network/$', views.get_network, name='network'),
)