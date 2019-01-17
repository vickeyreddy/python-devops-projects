import urllib, urllib2, sys, re, requests, json
from urllib2 import urlopen, HTTPError, URLError
from requests.exceptions import ConnectionError
from optparse import OptionParser


class GEIDM(object):

    admin_sso = 501874147
    admin_dl = "g00075565"
    req_user = "SPAPIADMIN"

    def __init__(self,subnet):
        self.subnet = subnet
        self.display_mail = 'NETProxy'+subnet+'@ge.com'

    def search_groupid(self):
        if not re.match("^(\d{3})\.(\d{3})\.(\d{3})\.(\d{3})\_(\d{2})$", self.subnet):
                data_dict = {'Error' : 'Invalid Subnet Address Given to Search'}
                return data_dict

        url = 'https://admin.idm.ge.com/groupapi/CDIFindGroups.jsp'
        params = { "mail": self.display_mail  }

        try:
            urlparams = urllib.urlencode(params)
            req = urllib2.Request(url, urlparams)
            res = urllib2.urlopen(req)
            data = res.read()
            match = re.compile("Success").search(data)
            data_dict = {}

            if match is None:
                data_dict = {'Error' : 'Subnet Does not Exist !!!'}
            else:
                result = data.replace('<br>', '').replace('ErrorResponse=0:Success', '').replace('DataResultSet=','').replace('\n', '').replace('\r', '')
                data_dict = dict(x.split('=') for x in result.split('^'))

        except urllib2.HTTPError, e:
            data_dict = { 'Error' : 'Unable to Connect to Server !!! HTTPError = ' + str(e.code)}
            return data_dict

        except urllib2.URLError, e:
            data_dict = {'Error' : 'Unable to Connect to Give URL !!! URLError = ' + str(e.reason)}
            return data_dict

        else:
            return data_dict

    def create_groupid(self, unit_id):
        if not re.match("^(\d{3})\.(\d{3})\.(\d{3})\.(\d{3})\_(\d{2})$", self.subnet):
                data_dict = {'Error' : 'Invalid Subnet Address Given to Search'}
                return data_dict

        try:
            url = "https://service.idm.ge.com/rest/ge/groupapi/createdl"
            payload = ("{\"groupDataArgs\": \n{\n\"deliveryrestrictions\": \"%s\", \n \"manager\": \"%s\", \n \"displayname\": \"NET Proxy %s\", \n \"description\": \"Autoproxy Subnet DL\", \n \"requestor\": \"SPAPIADMIN\", \n  \"mail\": \"%s\", \n  \"primarymanager\": \"%s\", \"securitygroup\": \"FALSE\", \"businessunitid\": \"%s\"}\n}" % (GEIDM.admin_dl, GEIDM.admin_sso, self.subnet, self.display_mail, GEIDM.admin_sso, unit_id))
            headers = {
                'authorization': "Basic R0VETE5XU19BRE1JTjpXM2JTZXJ2aWNlc0FyZWdyM2F0",
                'cache-control': "no-cache",
            }
            response = requests.request("POST", url, data=payload, headers=headers)
            data = response.text
            results = json.loads(data)
            data_dict = results['status'], results['errors']

        except ConnectionError as e:
            data_dict = { 'Error' : 'HTTPError = %s' % (e)}
            return data_dict

        else:
            return data_dict


    def delete_groupid(self, group_id):
        try:
            url = "https://service.idm.ge.com/rest/ge/groupapi/deletedl"

            payload = ("{\"groupDataArgs\":{\r\n\"groupid\":\"%s\",\r\n\"requestor\":\"SPAPIADMIN\"\r\n\t}\r\n}\r\n" % (group_id))

            headers = {
                'authorization': "Basic R0VETE5XU19BRE1JTjpXM2JTZXJ2aWNlc0FyZWdyM2F0",
                'content-type': "application/json",
                'cache-control': "no-cache",
            }
            response = requests.request("POST", url, data=payload, headers=headers)
            data = response.text
            results = json.loads(data)
            data_dict = results['status'], results['errors']

        except ConnectionError as e:
            data_dict = { 'Error' : 'HTTPError = %s' % (e)}
            return data_dict

        else:
            return data_dict
'''
if __name__ == '__main__':
        idm = GEIDM('999.999.999.999_99')
        result_create = idm.create_groupid('1750623')
        result_delete = idm.delete_groupid('g01144257')
        print result_create
'''
