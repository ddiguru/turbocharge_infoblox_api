#!/usr/bin/env python3

import argparse
import json
import logging
import os
import sys
import urllib3
from time import perf_counter

import aiohttp
import asyncio
import coloredlogs
from dotenv import load_dotenv
from netaddr import IPNetwork

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


def get_nets():
    base_network = IPNetwork('10.0.0.0/8')
    subnets = list(base_network.subnet(24, count=1024))
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


async def main():
    global s, url

    networks = get_nets()

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
