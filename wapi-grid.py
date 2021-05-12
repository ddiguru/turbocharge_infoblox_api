#!/usr/bin/env python3

import urllib3
import logging
import requests
from time import sleep

logging.basicConfig(level=logging.DEBUG)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

with requests.session() as s:
    s.verify = False
    url = 'https://192.168.40.58/wapi/v2.11/grid'

    s.get(url, auth=('admin', 'infoblox'), verify=False)

    while True:
        s.get(url, verify=False)
        sleep(1)
