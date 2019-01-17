#!/usr/bin/env python2.7 
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from ge_scalr import GEScalr
from dashboard.models import Farms, Environments, Servers, FarmsRoles, GEServers

def index(request):
	queryset = Servers.objects.all()
	envs = Environments.objects.all().count()
	frms = Farms.objects.all().count()
	frmroles = FarmsRoles.objects.all().count()
	servers = Servers.objects.all().count()
	context_dict = {
		'title': "Overview & Stats",
		'servers_list': queryset,
		'total_envs' : envs,
		'total_frms' : frms,
		'total_frmroles' : frmroles,
		'total_servers' : servers,
	}
	return render(request,'index.html',context=context_dict)

def farm_index(request):
	queryset = Farms.objects.all()
	context_dict = {
		'farm_list': queryset,
		'title': "Farms Overview"
	}
	return render(request,'farms.html',context=context_dict)


def env_index(request):
	queryset = Environments.objects.all() 
	data = {
		'env_list': queryset,
		'title': 'Environments Overview'
	}
	return render(request,'envs.html',data)


def frole_index(request):
	queryset = FarmsRoles.objects.all()
	context_dict = {
		'farmrole_list': queryset,
		'title': "FarmRoles Overview"
	}
	return render(request,'farmroles.html',context=context_dict)

def server_index(request):
	queryset = Servers.objects.all()
	context_dict = {
		'servers_list': queryset,
		'title': "Servers Overview"
	}
	return render(request,'servers.html',context=context_dict)

def gelan(request):
        queryset = GEServers.objects.all()
        context_dict = {
                'gelan_servers': queryset,
                'title': "Internal Applications Overview"
        }
        return render(request,'gelan_servers.html',context=context_dict)

def serverinfo(request, ip=None):
	s = Servers.objects.get(sip=ip)
	e = Environments.objects.get(env_name=s.ename)
	sid = get_object_or_404(Servers, sid=s.sid)
	c = GEScalr('https://scalr.corporate.ge.com/api/api.php', '9411fb3f576d99c5', 'neeBypT7o12N+i2neG3a6sAfrmYtAglatcZkQycBrYBd/9Vi4MlFHGT/hHA0Fz00ll5xnUyufZvExyzlFdVfgqyteh/pnNdRYxE60IQHmKQNrIyuEn57f4rPfdOUmGGv', 'EnvironmentsList', e.eid)
	sinfo = c.fetch_server_info(eid=e.eid,sid=s.sid)	
	context = {
		"sinfo": sinfo,
		'title': "Server Extended Information",
	}
	return render(request, "serverinfo.html", context)
