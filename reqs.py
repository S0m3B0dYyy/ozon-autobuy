import asyncio
import json
import random

import aiohttp
from fake_useragent import UserAgent
from loguru import logger

from loader import REQUEST_INTERVAL, REQUEST_ATTEMPTS, USE_PROXY

user_agent = UserAgent()

PROXIES = []


def load_proxies():
    global PROXIES
    if USE_PROXY == 1:
        try:
            with open('proxy.txt', 'r') as f:
                PROXIES = [line.strip() for line in f.readlines() if line.strip()]
                if not PROXIES:
                    logger.error("proxy.txt is empty")
        except FileNotFoundError:
            logger.error("proxy.txt not exists")


load_proxies()


async def getProxy():
    if USE_PROXY == 0:
        return None
    return random.choice(PROXIES)


async def get(session, url, params=None, json_res=False):
    last_response = None
    last_response_status = None
    for attempt in range(REQUEST_ATTEMPTS):
        current_proxy = await getProxy()
        try:
            async with session.get(url, params=params, proxy=current_proxy) as response:
                if json_res:
                    last_response = await response.json()
                else:
                    last_response = await response.text()
                last_response_status = response.status
                if response.status == 200:
                    return last_response
        except (aiohttp.ClientError, json.JSONDecodeError):
            pass
        if attempt < REQUEST_ATTEMPTS - 1:
            await asyncio.sleep(REQUEST_INTERVAL)
    logger.error(f'BAD REQUEST | {last_response_status} | {last_response}')
    return None


async def post(session, url, data={}, json_res=False):
    last_response = None
    last_response_status = None
    for attempt in range(REQUEST_ATTEMPTS):
        current_proxy = await getProxy()
        try:
            async with session.post(url, json=data, proxy=current_proxy) as response:
                if json_res:
                    last_response = await response.json()
                else:
                    last_response = await response.text()
                last_response_status = response.status
                if response.status == 200:
                    return last_response
        except Exception as e:
            pass
        if attempt < REQUEST_ATTEMPTS - 1:
            await asyncio.sleep(REQUEST_INTERVAL)
    logger.error(f'BAD REQUEST | {last_response_status} | {last_response}')
    return None
