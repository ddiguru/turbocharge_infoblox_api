#!/usr/bin/env python3

import os
import sys
import json
import urllib3
import logging
import argparse
import requests
import coloredlogs
from netaddr import IPNetwork
from time import perf_counter, sleep

load_dotenv()

__author__ = 'ppiper'
ibx_grid_master = '192.168.40.58'
ibx_username = 'admin'
ibx_password = 'infoblox'
ibx_wapi_version = 'v2.11'

log_level = logging.DEBUG
log_format = '%(asctime)s %(levelname)s %(message)s'
logger = logging.getLogger()
coloredlogs.install(
    level=log_level,
    logger=logger,
    fmt=log_format
)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_nets():
    base_network = IPNetwork('10.0.0.0/8')
    subnets = list(base_network.subnet(24, count=1024))
    return subnets


def main():
    url = f'https://{ibx_grid_master}/wapi/{ibx_wapi_version}'
    with requests.session() as s:
        grid = s.get(f'{url}/grid', auth=(ibx_username, ibx_password), verify=False)
        logger.info(grid.json())

    networks = get_nets()

    t1_start = perf_counter()

    # add networks using the requests object
    network_requests = []
    for network in networks:
        network_object = dict(
            method="POST",
            object="network",
            data=dict(network=str(network), comment='test-network')
        )
        network_requests.append(network_object)

    s.post(f'{url}/request', data=json.dumps(network_requests), verify=False)

    t1_stop = perf_counter()

    logger.info('finished!')
    logger.info(f'elapsed time for execution {t1_start - t1_stop}')

    sys.exit()


if __name__ == '__main__':
    main()
