#!/usr/bin/env python2.7

import datetime, urllib, urllib2, base64, hmac, hashlib, os, sys, re
import xml.etree.ElementTree as ET
from urllib2 import urlopen, HTTPError, URLError

class GEScalr(object):

    api_version = '2.3.0'
    api_auth_version = '3'

    def __init__(self, api_url, api_key, api_skey, api_action, env_id):

        self.api_url = api_url
        self.api_key = api_key
        self.api_skey = api_skey
        self.api_action = api_action
        self.env_id = env_id
        self.params = {
            "Action": api_action,
            "Version": GEScalr.api_version,
            "AuthVersion": GEScalr.api_auth_version,
            "KeyID": api_key,
        }

    def set_params(self, action):

        self.api_action = action
        timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        signature = base64.b64encode(hmac.new(self.api_skey, ":".join([self.api_action, self.api_key, timestamp]), hashlib.sha256).digest())
        self.params["EnvID"] = self.env_id
        self.params["Action"] = self.api_action
        self.params["Timestamp"] = timestamp
        self.params["Signature"] = signature
                
        try:
            urlparams = urllib.urlencode(self.params)
            req = urllib2.Request(self.api_url, urlparams)
            res = urllib2.urlopen(req)
            data = res.read()
            
        except urllib2.HTTPError, e:
            print ('HTTPError = ' + str(e.code))

        except urllib2.URLError, e:
            print ('URLError = ' + str(e.reason))
            
        else:
            return data


    def fetch_envs(self):

        data = self.set_params('EnvironmentsList')

        try:

            match = re.compile("<EnvironmentSet>(.*)</EnvironmentSet>").search(data).group(0)
            root = ET.fromstring(match)
            envs = {}
            techsolns_envs = {}
            pattern = re.compile('techsolns')

            for env_id, env_name in zip(root.iter('ID'), root.iter('Name')):
                  envs[env_name.text] = env_id.text

            for key, value in envs.iteritems():
                  if pattern.search(key):
                       techsolns_envs[key] = value
                       
        except AttributeError:
               pass

        else:
               return techsolns_envs


    def fetch_farms(self, envid):

        self.env_id = envid 
        data = self.set_params('FarmsList')

        try:

            match = re.compile("<FarmSet>(.*)</FarmSet>").search(data).group(0)
            root = ET.fromstring(match)
            farms = {}

            for farm_id, farm_name, farm_comment, farm_status in zip(root.iter('ID'), root.iter('Name'), root.iter('Comments'), root.iter('Status')):
                farms[farm_id.text] = [self.env_id, farm_name.text, farm_comment.text, farm_status.text]
        
        except AttributeError:
               pass

        else:
               return farms


    def fetch_farmroles(self, frmid=None):

        self.frmid = frmid
        self.params["FarmID"] = self.frmid 
        data = self.set_params('FarmGetDetails')

        try:

            match = re.compile("<FarmRoleSet>(.*)</FarmRoleSet>").search(data).group(0)
            root = ET.fromstring(match)
            farmroles = {}

            for fid, frname, falias, fmin, fmax in zip(root.iter('ID'), root.iter('Name'), root.iter('Alias'), root.iter('MinInstances'), root.iter('MaxInstances')):
                   farmroles[fid.text] = [ self.env_id, frname.text, falias.text, fmin.text, fmax.text ]
    
        except AttributeError:
               pass

        else:
               return farmroles
            
    def fetch_servers(self, frmid=None):

        self.frmid = frmid
        self.params["FarmID"] = self.frmid 
        data = self.set_params('FarmGetDetails')

        try:
            match = re.compile("<FarmRoleSet>(.*)</FarmRoleSet>").search(data).group(0)
            root = ET.fromstring(match)
            servers = {}

            for sid, iip, status, uptime, itype in zip(root.iter('ServerID'), root.iter('InternalIP'), root.iter('Status'), root.iter('Uptime'), root.iter('InstanceType')):
                    servers[sid.text] = [ self.env_id, self.frmid, iip.text, status.text, uptime.text, itype.text ]
            
        except AttributeError:
               pass
            
        else:
               return servers

    def fetch_server_info(self, eid=None, sid=None):

        self.sid = sid
	self.eid = eid
        self.params["ServerID"] = self.sid 
        self.params["EnvID"] = self.eid
        data = self.set_params('ServerGetExtendedInformation')

        try:
            match = re.compile("<ServerGetExtendedInformationResponse>(.*)</ServerGetExtendedInformationResponse>").search(data).group(0)
            root = ET.fromstring(match)
            server_info = {}
	    
	    for s in root.iter():
                    server_info[s.tag] = [ s.text ]
            
        except AttributeError:
               pass
            
        else:
               return server_info

'''
    def fetch_servers_graph(self, server_id='', object_name='server', watcher_type='CPU', graph_type='weekly'):self.server_id = server_id
        self.object_name = object_name
        self.graph_type = graph_type
        self.watcher_type = watcher_type
        data = self.set_params('StatisticsGetGraphURL')
        data = self.set_params('ObjectID')
	data["ObjectID"] = self.server_id 
        data = self.set_params('WatcherName')
	data["WatcherName"] = self.watcher_type
        data = self.set_params('GraphType')
	data["GraphType"] = self.graph_type
        data = self.set_params('ObjectType')
	data["ObjectType"] = self.object_name
        try:
            match = re.compile("<GraphURL>(.*)</GraphURL>").search(data).group(0)
            root = ET.fromstring(match)
            server_url = {}

            for url in root.iter(''):
                    server_url['server_id'] = url.text
        except AttributeError:
               pass
        else:
               return server_url
	       print server_url
'''
