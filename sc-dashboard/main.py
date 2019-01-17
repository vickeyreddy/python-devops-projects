from sep_api import DashboardSC
from sc_api import DashboardSC

api = SEP_Dashboard(authapi='https://192.168.1.1:8446/sepm/api/v1/identity/authenticate', apiuser='user1', apipass='pass1')
api.app()
