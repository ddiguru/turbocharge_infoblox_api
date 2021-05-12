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

__author__ = 'ppiper'
ibx_grid_master = '192.168.1.2'
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


def get_nets(block='10.0.0.0/8', cidr=24, num_of_networks=1024):
    base_network = IPNetwork(block)
    subnets = list(base_network.subnet(cidr, count=num_of_networks))
    return subnets


def get_args():
    parser = argparse.ArgumentParser(description='script description')
    parser.add_argument('-b', '--block', help='network block in CIDR form to build list from')
    parser.add_argument('-c', '--cidr', type=int, help='size of networks to build (int)')
    parser.add_argument('-n', '--number', type=int, help='number of consecutive subnets to create')
    return parser.parse_args()


def main():
    args = get_args()
    ip_block = args.block or '10.0.0.0/8'
    size_of_networks = args.cidr or 24
    num_of_networks = args.number or 1024

    url = f'https://{ibx_grid_master}/wapi/{ibx_wapi_version}'
    with requests.session() as s:
        grid = s.get(f'{url}/grid', auth=(ibx_username, ibx_password), verify=False)
        logger.info(grid.json())

    networks = get_nets(ip_block, size_of_networks, num_of_networks)

    t1_start = perf_counter()

    # create IPv4 Network object(s) one at a time
    for network in networks:
        payload = dict(network=network, comment='test-network')
        s.post(f'{url}/network', data=json.dumps(payload), verify=False)
    
    t1_stop = perf_counter()

    logger.info('finished!')
    logger.info(f'elapsed time for execution {t1_start - t1_stop}')

    sys.exit()


if __name__ == '__main__':
    main()
