import asyncio
import uuid
from datetime import datetime, timedelta

import aiohttp
from loguru import logger

import reqs
from loader import ACCESS_TOKEN, REFRESH_TOKEN, ABT_DATA, SKU_ID, SKU_QUANTITY, HOURS, MINUTES, SECONDS, MILLISECONDS, \
    ORDER_INTERVAL, ORDER_ATTEMPTS, USE_START_TIME, USE_MEASURING, ADD_TO_CART
from utils import measure_time, generate_x_o3_fp_ozon

order_data = [
    {
        "id": SKU_ID,
        "quantity": SKU_QUANTITY
    }
]

COOKIES = {
    'x-o3-app-name': 'ozonapp_android',
    'x-o3-app-version': '17.40.1(2517)',
    'MOBILE_APP_TYPE': 'ozonapp_android',
    '__Secure-access-token': ACCESS_TOKEN,
    '__Secure-refresh-token': REFRESH_TOKEN,
    'abt_data': ABT_DATA,
}

HEADERS = {
    'host': 'api.ozon.ru',
    'x-o3-fp': generate_x_o3_fp_ozon(),
    'user-agent': 'ozonapp_android/17.40.1+2517',
    'x-o3-app-name': 'ozonapp_android',
    'x-o3-app-version': '17.40.1(2517)',
    'x-o3-sample-trace': 'false',
    'mobile-gaid': str(uuid.uuid4()),
    'mobile-lat': '0',
    'x-o3-device-type': 'tablet',
    'accept': 'application/json; charset=utf-8',
    'content-type': 'application/json; charset=UTF-8',
    'cookie': "; ".join([f"{k}={v}" for k, v in COOKIES.items()]),
}


@measure_time(USE_MEASURING)
async def addToCart(session, data):
    res = await reqs.post(
        session,
        'https://api.ozon.ru/composer-api.bx/_action/addToCart',
        data
    )
    if res:
        logger.info('ADD TO CART')
    return res


@measure_time(USE_MEASURING)
async def refreshCart(session):
    res = await reqs.get(
        session,
        'https://api.ozon.ru/composer-api.bx/page/json/v2',
        {
            'url': '/cart?refresh=true'
        }
    )
    if res:
        logger.info('REFRESH CART')
    return res


@measure_time(USE_MEASURING)
async def goToCheckout(session):
    res = await reqs.get(
        session,
        'https://api.ozon.ru/composer-api.bx/page/json/v2',
        {
            'url': f'/gocheckout?start=0&activeTab=0&session_uid={uuid.uuid4()}',
            'nativePaymentEnabled': 'true',
            'nativePaymentConfigured': 'false',
            'deviceId': str(uuid.uuid4())
        }
    )
    if res:
        logger.info('GO TO CHECKOUT')
    return res


@measure_time(USE_MEASURING)
async def createOrder(session):
    res = await reqs.post(
        session,
        'https://api.ozon.ru/composer-api.bx/_action/v2/createOrder'
    )
    if res:
        logger.info('CREATE ORDER')
    return res


async def main():
    if USE_START_TIME == 1:
        now = datetime.now()
        target_time = now.replace(hour=HOURS, minute=MINUTES, second=SECONDS,
                                  microsecond=MILLISECONDS)

        if target_time < now:
            target_time += timedelta(days=1)

        wait_seconds = (target_time - now).total_seconds()
        logger.info(
            f"START AT {HOURS:02}:{MINUTES:02}:{SECONDS:02}:{MILLISECONDS:02} | WAIT {wait_seconds:.2f} seconds")
        await asyncio.sleep(wait_seconds)
    else:
        logger.warning(f"USE_START_TIME IS DISABLED")

    async with (aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False),
            headers=HEADERS,
            trust_env=True
    ) as session):
        if ADD_TO_CART == 1:
            for _ in range(ORDER_ATTEMPTS):
                await asyncio.gather(
                    addToCart(session, order_data),
                    refreshCart(session),
                    goToCheckout(session),
                    createOrder(session)
                )
        else:
            for _ in range(ORDER_ATTEMPTS):
                await asyncio.gather(
                    refreshCart(session),
                    goToCheckout(session),
                    createOrder(session)
                )

        await asyncio.sleep(ORDER_INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())
