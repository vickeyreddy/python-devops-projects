from django.conf.urls import url
from django.contrib import admin
from dashboard.views import main

urlpatterns = [
	url(r'^$', main.index, name='index'),
	url(r'^farms/$', main.farm_index, name='farms'),
	url(r'^farmroles/$', main.frole_index, name='farmroles'),
	url(r'^envs/$', main.env_index, name='env'),
	url(r'^servers/$', main.server_index, name='server'),
	url(r'^serverinfo/(?P<ip>(\d{2})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3}))/$', main.serverinfo, name='serverinfo'),
	url(r'^gelanservers/$', main.gelan, name='gelan'),
]

