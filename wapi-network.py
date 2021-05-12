#!/usr/bin/env python3

import os
import sys
import json
import urllib3
import logging
import argparse
import requests
import coloredlogs
from dotenv import load_dotenv
from netaddr import IPNetwork
from time import perf_counter, sleep

load_dotenv()

__author__ = 'ppiper'
s = None
url = ''
ibx_grid_master = os.getenv('ibx_gridmaster')
ibx_username = os.getenv('ibx_username')
ibx_password = os.getenv('ibx_password')
ibx_wapi_version = os.getenv('ibx_wapi_version')

log_level = logging.DEBUG
log_format = '%(asctime)s %(levelname)s %(message)s'
logger = logging.getLogger()
coloredlogs.install(
    level=log_level,
    logger=logger,
    fmt=log_format
)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def insert_network(network):
    payload = dict(network=network, comment='test-network')
    s.post(f'{url}/network', data=json.dumps(payload), verify=False)


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
    global s, url
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
    for network in networks:
        insert_network(str(network))
    t1_stop = perf_counter()

    logger.info('finished!')
    logger.info(f'elapsed time for execution {t1_start - t1_stop}')

    sys.exit()


if __name__ == '__main__':
    main()
