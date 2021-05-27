#!/usr/bin/env python3

import argparse
import json
import logging
import os
import sys
from time import perf_counter

import aiohttp
import asyncio
import coloredlogs
from dotenv import load_dotenv
from netaddr import IPNetwork

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


def get_nets(block='10.0.0.0/8', cidr=24, num_of_networks=1024):
    base_network = IPNetwork(block)
    subnets = list(base_network.subnet(cidr, count=num_of_networks))
    return subnets


async def load_network(sem, session, network):
    async with sem:
        await fetch(session, network)


async def fetch(session, network):
    payload = dict(network=str(network), comment='test-network')
    async with session.post(f'{url}/network', data=payload, ssl=False) as res:
        if res.status == 201:
            logger.info(f'successfully inserted network {str(network)}')
        else:
            logger.error(f'failed to load network {str(network)}')


def get_args():
    parser = argparse.ArgumentParser(description='script description')
    parser.add_argument('-b', '--block', help='network block in CIDR form to build list from')
    parser.add_argument('-c', '--cidr', type=int, help='size of networks to build (int)')
    parser.add_argument('-n', '--number', type=int, help='number of consecutive subnets to create')
    return parser.parse_args()


async def main():
    global s, url
    args = get_args()
    ip_block = args.block or '10.0.0.0/8'
    size_of_networks = args.cidr or 24
    num_of_networks = args.number or 1024

    networks = get_nets(ip_block, size_of_networks, num_of_networks)

    url = f'https://{ibx_grid_master}/wapi/{ibx_wapi_version}'

    t1_start = perf_counter()

    auth = aiohttp.BasicAuth(login=ibx_username, password=ibx_password)
    async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True)) as session:
        async with session.get(f'{url}/grid', auth=auth, ssl=False) as res:
            logger.debug(res.status)
            tasks = []
            sem = asyncio.Semaphore(16)
            for network in networks:
                task = asyncio.ensure_future(load_network(sem, session, network))
                tasks.append(task)

            responses = asyncio.gather(*tasks)
            await responses

    t1_stop = perf_counter()

    logger.info('finished!')
    logger.info(f'elapsed time for execution {t1_start - t1_stop}')

    sys.exit()


loop = asyncio.get_event_loop()
future = asyncio.ensure_future(main())
loop.run_until_complete(future)
