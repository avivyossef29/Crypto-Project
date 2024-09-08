import requests
import ssl
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

response = session.post(url="https://server-demo/?username=victim", \
                        cookies={"secret-cookie": "test"}, \
                        headers={"Content-Type":"application/json"}, \
                        data={"data": "it worked!!!!"}, \
                        verify=False)

print(response.text)