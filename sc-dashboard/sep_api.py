import json, sys, os, requests, time, calendar
from urllib2 import urlopen, HTTPError, URLError
from optparse import OptionParser
from datetime import datetime, timedelta
from mysql import MySQL

class DashboardSC(object):

    tdate = datetime.today()
    ydate = tdate - timedelta(1)
    start_date = tdate.strftime("%Y-%m-%d")
    end_date = ydate.strftime("%Y-%m-%d")
    api_today = calendar.timegm(time.gmtime())
    api_yesterday = (api_today - 84000)

    def __init__(self, authapi, apiuser, apipass, domain=None, apidomain=None, dbname='dashboard', dbhost='localhost', dbport=3306, dbuser='powerbi', dbpass='powerbi'):

        self.authapi = authapi
        self.apiuser = apiuser
        self.apipass = apipass
        self.apidomain = apidomain
        self.dbname = dbname
        self.dbhost = dbhost
        self.dbport = dbport
        self.dbuser = dbuser
        self.dbpass = dbpass
        self.domain = domain
        self.payload = {
            "username": self.apiuser,
            "password": self.apipass,
            "domain": self.domain
        }
        self.headers = {
            "Content-type": 'application/json'
        }

        try:
            r = requests.post(self.authapi, data=json.dumps(self.payload), headers=self.headers, verify=False)
            s = json.loads(r.text)
        except requests.exceptions.RequestException as e:
            print(e)
        else:
            self.token = "Bearer " + s['token']
            self.db = MySQL(host=self.dbhost, port=self.dbport, user=self.dbuser, passwd=self.dbpass, dbname=self.dbname)

    def get_rest_api_data(self, rest_api):
        rapi_headers = {
                 "Authorization": self.token,
                 "Content-type": 'application/json'
        }

        try:
            req = requests.get(rest_api, headers=rapi_headers, verify=False)
            data = json.loads(req.text)
        except requests.exceptions.RequestException as e:
            print(e)
        else:
            return data

    def get_risk_count(self):
        api = ("https://10.202.30.21:8446/sepm/api/v1/stats/client/risk/%s/to/%s" % (SEP_Dashboard.api_yesterday, SEP_Dashboard.api_today))
        data = self.get_rest_api_data(api)
        if len(data["riskDistributionStats"]) is None:
            print("risk_distribution_stats is Empty")
            sys.exit(-1)
        else:
            tq = "risk_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, risk_count INT(5) NOT NULL, protection_name VARCHAR(30) NOT NULL, client_count INT(10) NOT NULL, start_date DATE, end_date DATE"
            self.db.create_table(table='risk_distribution_stats', tquery=tq)
            for l in range(0,len(data["riskDistributionStats"])):
                for v in data.itervalues():
                    sq = "INSERT INTO risk_distribution_stats(risk_count, protection_name, client_count, start_date, end_date) VALUES ('%d', '%s', '%d', '%s', '%s' )" % (v[l]["riskCount"], v[l]["protectionName"], v[l]["protectionEnabledClientCount"], SEP_Dashboard.start_date, SEP_Dashboard.end_date)
                    self.db.insert_data(squery=sq)
            return "Records sucessfully updated"

    def get_autoresolved_count(self):
        api = ("https://10.202.30.21:8446/sepm/api/v1/stats/autoresolved/Day/%s/to/%s" % (SEP_Dashboard.api_yesterday, SEP_Dashboard.api_today))
        data = self.get_rest_api_data(api)
        if len(data["autoResolvedAttacks"]) is None:
            print("Auto Resolved Attacks is Empty")
            sys.exit(-1)
        else:
            tq = 'auto_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, threat_count INT(10) NOT NULL, start_date DATE, end_date DATE'
            self.db.create_table(table='autoresolved_count', tquery=tq)
            for v in data["autoResolvedAttacks"]:
                sql = "INSERT INTO autoresolved_count(threat_count, start_date, end_date) VALUES('%d', '%s', '%s')" % (v["autoResolvedAttacksCount"], SEP_Dashboard.start_date, SEP_Dashboard.end_date)
                self.db.insert_data(squery=sql)
            return "Records successfully updated"

    def get_malware_count(self):
        api = ("https://10.202.30.21:8446/sepm/api/v1/stats/client/malware/Day/%s/to/%s" % (SEP_Dashboard.api_yesterday, SEP_Dashboard.api_today))
        data = set_rest_api_token(api)
        if len(data["malware_count"]) is None:
            print("malware_count is Empty")
            sys.exit(-1)
        else:
            tq = ''
            self.db.create_table(table='risk_distribution_stats', tquery=tq)
            for l in range(0,data_size):
                for v in data.itervalues():
                    sql = "INSERT INTO malware_count(malware_id, client_count, start_date, end_date VALUES ('%d', '%d', '%s', '%s' )" % (v[l]["malware_id"], v[l]["client_count"], start_date, end_date)
                    self.db.insert_data(squery=sq)
            return "Records successfully updated"

    def get_versionlist_stats(self):
        api = ("https://10.202.30.21:8446/sepm/api/v1/stats/client/version")
        data = set_rest_api_token(api)
        if len(data["versionlist_stats"]) is None:
            print("versionlist_stats is Empty")
            sys.exit(-1)
        else:
            tq = ''
            self.db.create_table(table='risk_distribution_stats', tquery=tq)
            for l in range(0,data_size):
                for v in data.itervalues():
                    sql = "INSERT INTO versionlist_stats(version_id, version, client_count, start_date, end_date VALUES ('%d', '%s', '%d', '%s', '%s' )" % (v[l]["version_id"], v[l]["version"], v[l]["client_count"], start_date, end_date)
                    self.db.insert_data(squery=sq)
            return "Records successfully updated"

    def get_infectedclient_count(self):
        api = ("https://10.202.30.21:8446/sepm//api/v1/stats/client/infection/Day/%s/to/%s" % (SEP_Dashboard.api_yesterday, SEP_Dashboard.api_today))
        data = set_rest_api_token(api)
        if len(data["riskDistributionStats"]) is None:
            print("risk_distribution_stats is Empty")
            sys.exit(-1)
        else:
            tq = ''
            self.db.create_table(table='risk_distribution_stats', tquery=tq)
            for l in range(0,data_size):
                for v in data.itervalues():
                    sql = "INSERT INTO infectedclient_count(infected_id, client_count, start_date, end_date VALUES ('%d', '%d', '%s', '%s' )" % (v[l]["infected_id"], v[l]["client_count"], start_date, end_date)
                    self.db.insert_data(squery=sq)
            return "Records successfully updated"

    def app(self):
        self.get_risk_count()
        self.get_malware_count()
        self.get_infectedclient_count()
        self.get_versionlist_stats()
        self.get_autoresolved_count()
