import requests
import ssl
import time
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

requests.packages.urllib3.disable_warnings() 

class SSL3Adapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        #context = ssl.SSLContext(ssl.PROTOCOL_SSLv3)
        kwargs['ssl_version'] = ssl.PROTOCOL_SSLv3
        return super(SSL3Adapter, self).init_poolmanager(*args, **kwargs)

# Create a session and mount the adapter
session = requests.Session()
session.mount('https://', SSL3Adapter())

for i in range(1):
    time.sleep(3)
    response = session.post(url="https://server_container/login?username=victim&password=12345", \
                            headers={"Content-Type":"application/json"}, \
                            verify=False)

print(response.text)