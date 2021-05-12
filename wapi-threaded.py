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
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()

__author__ = 'ppiper'
ibx_grid_master = '192.168.40.58'
ibx_username = 'admin'
ibx_password = 'infoblox'
ibx_wapi_version = 'v2.11'
s = None
url = ''
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
    try:
        res = s.post(f'{url}/network', data=json.dumps(payload), verify=False)
        return res.status_code
    except Exception as e:
        return e


def get_nets():
    base_network = IPNetwork('10.0.0.0/8')
    subnets = list(base_network.subnet(24, count=1024))
    return subnets


def runner(networks):
    threads = []
    with ThreadPoolExecutor(max_workers=16) as executor:
        for network in networks:
            threads.append(executor.submit(insert_network, str(network)))

        for task in as_completed(threads):
            print(task.result())
            if task.result() == 201:
                logger.info('thread successfully inserted network')
            else:
                logger.warning('thread failed to insert network')


def main():
    global s, url
    url = f'https://{ibx_grid_master}/wapi/{ibx_wapi_version}'
    with requests.session() as s:
        grid = s.get(f'{url}/grid', auth=(ibx_username, ibx_password), verify=False)
        logger.info(grid.json())

    networks = get_nets()

    t1_start = perf_counter()
    runner(networks)
    t1_stop = perf_counter()

    logger.info('finished!')
    logger.info(f'elapsed time for execution {t1_start - t1_stop}')

    sys.exit()


if __name__ == '__main__':
    main()
