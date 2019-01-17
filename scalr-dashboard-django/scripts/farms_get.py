import datetime, urllib, base64, hmac, hashlib, os, sys, re
import xml.dom.minidom as ET
import xml.etree.ElementTree as ET

class GEScalr(object):

    def __init__(self, api_url, api_key, api_skey, api_action, env_id):

        self.api_url = api_url
        self.api_key = api_key
        self.api_skey = api_skey
        self.api_action = api_action
        self.env_id = env_id
        self.api_version = '2.3.0'
        self.api_auth_version = '3'

    #def params(self):
    def list_environments(self):
        timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        params = { "Action": self.api_action,
                   "Version": self.api_version,
                   "AuthVersion": self.api_auth_version,
                   "Timestamp": timestamp,
                   "KeyID": self.api_key,
                   "EnvID": self.env_id,
                   "Signature":  base64.b64encode(hmac.new(self.api_skey, ":".join([self.api_action, self.api_key, timestamp]), hashlib.sha256).digest()),
                  }
        urlparams = urllib.urlencode(params)
	print urlparams
        req = urllib.urlopen(self.api_url, urlparams)
	print req
        base = req.read()
	print base
        match = re.compile("<EnvironmentSet>(.*)</EnvironmentSet>").search(base).group(0)
        root = ET.fromstring(match)
        envs = {}
        for env_id, env_name in zip(root.iter('ID'), root.iter('Name')):
            envs[env_name.text] = env_id.text
        return envs

        #params = re.compile('techsolns')
        #envs_dict = {}
        #for key, value in envs.iteritems():
        #       if params.search(key):
        #               print key, value

if __name__ == "__main__":

    c = GEScalr('https://scalr.corporate.ge.com/api/api.php', '9411fb3f576d99c5', 'neeBypT7o12N+i2neG3a6sAfrmYtAglatcZkQycBrYBd/9Vi4MlFHGT/hHA0Fz00ll5xnUyufZvExyzlFdVfgqyteh/pnNdRYxE60IQHmKQNrIyuEn57f4rPfdOUmGGv', 'EnvironmentsList', 52)
    print c.list_environments()

