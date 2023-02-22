import asyncio
import platform
import logging
from pprint import pprint

import aiohttp

async def request(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    r = await response.json()
                    return r
                logging.error(f"Error status {response.status} for {url}")
        except aiohttp.ClientConnectorError as e:
            logging.error(f"Connection error {url}: {e}")
        return None


async def get_exchange(date):
    res = await request(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}')
    return res


def exchange_on_date():
    res = {}
    lst_exc = {'EUR' : 0, 'USD': 0}
    cur_eur = {'sale': 0, 'purchase': 0}
    cur_usd = {'sale': 0, 'purchase': 0}
    for val in r['exchangeRate']:
        if val['currency'] == 'EUR':
            cur_eur['sale'] = val['saleRate']
            cur_eur['purchase'] = val['purchaseRate']
        if val['currency'] == 'USD':
            cur_usd['sale'] = val['saleRate']
            cur_usd['purchase'] = val['purchaseRate']
    lst_exc['EUR'] = cur_eur
    lst_exc['USD'] = cur_usd
    res[r['date']] = lst_exc
    return res

if __name__ == "__main__":
    dates = ['21.02.2023','22.02.2023']
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    for date in dates:
        r = asyncio.run(get_exchange(date))
        exc = exchange_on_date()
        print(exc)
    # pprint(r)
