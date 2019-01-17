#!/usr/bin/env python2.7

from ge_scalr import GEScalr
import django,sys,os

sys.path.append("/appl/GEScalr")
os.environ["DJANGO_SETTINGS_MODULE"] = "GEScalr.settings"
django.setup()

from dashboard.models import Environments, Farms, FarmsRoles, Servers

##### Creating an instance of GEScalr Class #####
c = GEScalr('https://scalr.corporate.ge.com/api/api.php', '9411fb3f576d99c5', 'neeBypT7o12N+i2neG3a6sAfrmYtAglatcZkQycBrYBd/9Vi4MlFHGT/hHA0Fz00ll5xnUyufZvExyzlFdVfgqyteh/pnNdRYxE60IQHmKQNrIyuEn57f4rPfdOUmGGv', 'EnvironmentsList', 53)

##### Fetching Environments Details #####
envs = c.fetch_envs()
for key, value in envs.items():
	env = Environments(eid=value, env_name=key)
	env.save()
        print ("Successfully Added: EnvironmentName: %s EnvironmentID: %s" % (key,value))

##### Fetching Farms Details Of All Environments #####
for enm,eid in envs.iteritems():
	farms = c.fetch_farms(eid)
	for k,v in farms.iteritems():
		if v[3] == '1':
			v[3] = 'Running'
		else:
			v[3] = 'Stopped' 
		frm = Farms(fid=k, ename=enm, f_name=v[1], f_dis=v[2], f_status=v[3])
		frm.save()
		print ("FarmName: %s Successfully Addedd!!!" % (v[1]))

##### Fetching Farm Roles Details of all Farms in all environments #####
for enm,eid in envs.iteritems():
	farms = c.fetch_farms(eid)	
	for fk,fv in farms.iteritems():
		frms = c.fetch_farmroles(fk)
		if frms == None:
			pass
		else:
			for frk, frv in frms.iteritems():
				frmrole = FarmsRoles(rid=frk, ename=enm, fname=fv[1], r_name=frv[1], r_alias=frv[2], r_min=frv[3], r_max=frv[4])
				frmrole.save()
				print ("FarmRole: %s Sucessfully Added!!!" % (frv[2]))

##### Fetching Servers Details from specific environments, farms and farmroles #####
ServerList = Servers.objects.filter(s_status="Terminated").delete()
for enm,eid in envs.iteritems():
	farms = c.fetch_farms(eid)	
	for fk,fv in farms.iteritems():
		servers = c.fetch_servers(fk)
		if servers == None:
			pass
		else:
			for sk, sv in servers.iteritems():
				srv = Servers(sid=sk, ename=enm, fname=fv[1], frname=fv[2], sip=sv[2], s_status=sv[3], uptime=sv[4], s_type=sv[5])
				srv.save()
				print ("Server sucessfully %s %s!!!" % (sk, sv[2]))

##### Fetching Servers Details from specific environments, farms and farmroles #####
for enm,eid in envs.iteritems():
	farms = c.fetch_farms(eid)	
	for fk,fv in farms.iteritems():
		servers = c.fetch_servers(fk)
		if servers == None:
			pass
		else:
			for sk, sv in servers.iteritems():
				server_info = c.fetch_server_info(sid=sk)
'''
##### Fetching Servers Details from specific environments, farms and farmroles #####
def server_extended_info(eid,sid):
	server_info = c.fetch_server_info(sid=sid,eid=eid)
	return server_info
'''
