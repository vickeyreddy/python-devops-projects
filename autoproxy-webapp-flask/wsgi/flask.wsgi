import sys
import os

activate_this = '/appl/webdocs/autoproxy/autoproxy_venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

sys.stdout = sys.stderr

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..'))

sys.path.append('/appl/webdocs/autoproxy/')
 
from autoproxy.main import app as application
application.secret_key = 'DevOps@2016'
