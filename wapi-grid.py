#!/usr/bin/env python3

import urllib3
import logging
import requests
from time import sleep

logging.basicConfig(level=logging.DEBUG)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ibx_grid_master = '192.168.40.58'
ibx_username = 'admin'
ibx_password = 'infoblox'
ibx_wapi_version = 'v2.11'

with requests.session() as s:
    s.verify = False
    url = f'https://{ibx_grid_master}/wapi/{ibx_wapi_version}/grid'

    s.get(url, auth=(ibx_username, ibx_password), verify=False)

    while True:
        s.get(url, verify=False)
        sleep(1)
