#!/usr/bin/env python3

import requests
from time import sleep
import urllib3
import logging
logging.basicConfig(level=logging.DEBUG)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

s = requests.session()
s.verify = False
url = 'https://192.168.1.2/wapi/v2.11/grid'

s.get(url, auth=('admin','infoblox'), verify=False)

while True:
    s.get(url, verify=False)
    sleep(1)