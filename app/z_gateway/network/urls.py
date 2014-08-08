from django.conf.urls import patterns, url

from network import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^get_start_status/$', views.network_get_start_status, name='get_status'),
    url(r'^get_state/$', views.network_get_state, name='get_state'),
    url(r'^get_timeout/$', views.network_get_timeout, name='get_timeout'),
    url(r'^start_network/$', views.start_network, name='start_network'),
    url(r'^stop_network/$', views.stop_network, name='stop_network'),
    url(r'^get_home_id/$', views.get_home_id, name='get_home_id'),
)