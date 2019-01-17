from __future__ import unicode_literals
from django.db import models
from django.utils import timezone


class Environments(models.Model):
	eid = models.IntegerField(unique=False, primary_key=True)
	env_name = models.CharField(max_length=200)

    	def __unicode__(self):
        	return self.env_name

class Farms(models.Model):
	fid = models.IntegerField(unique=False, primary_key=True)
        ename = models.CharField(max_length=200, blank=True, null=True)
        f_name = models.CharField(max_length=200,blank=True, null=True)
        f_dis = models.CharField(max_length=200, blank=True, null=True)
        f_status = models.CharField(max_length=20)
    	
	def __unicode__(self):
        	return self.f_name

class FarmsRoles(models.Model):
        rid = models.IntegerField(unique=False, primary_key=True)
	ename = models.CharField(max_length=200)
	fname = models.CharField(max_length=200, blank=True, null=True)
	r_name = models.CharField(max_length=200, blank=True, null=True)
        r_alias = models.CharField(max_length=200, blank=True, null=True)
        r_min = models.IntegerField()
        r_max = models.IntegerField()

	def __unicode__(self):
        	return self.r_name

class GEServers(models.Model):
	sid = models.AutoField(primary_key=True)
	appname = models.CharField(max_length=200, blank=False, null=False)
	ename = models.CharField(max_length=200, blank=False, null=False)
        hostname = models.CharField(max_length=200, blank=False, null=False)
        status = models.CharField(max_length=200, blank=False, null=False)
	
	def __unicode__(self):
                return self.hostname

class Servers(models.Model):
	sid = models.CharField(max_length=200, unique=False, primary_key=True)
	ename = models.CharField(max_length=200)
	fname = models.CharField(max_length=200, blank=True, null=True)
        frname = models.CharField(max_length=200, blank=True, null=True)
        sip = models.CharField(max_length=200, blank=True, null=True)
        s_status = models.CharField(max_length=200)
        uptime = models.CharField(max_length=200, blank=True, null=True)
        s_type = models.CharField(max_length=200, blank=True, null=True)
	
	def __unicode__(self):
                return self.sip

