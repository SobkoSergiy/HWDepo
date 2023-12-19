import platform
import asyncio
import aiohttp
import sys      
# import json
from datetime import datetime, timedelta
from colorama import init, Fore 


def help_prn():
    print('''
    PB_rates [days][currency]
    days = integer 1..10 (default = 1)
    currency = USD EUR CHF GBP PLZ SEK CAD XAU       
    in any combination (default = all): 
        USD	долар США
        EUR	євро
        CHF	швейцарський франк
        GBP	британський фунт
        PLZ	польський злотий
        SEK	шведська крона
        CAD	канадський долар
        XAU	золото
    ?, -h - this text   
    ''')


async def clean_data(data, curr):
    res = []
    for el in data:
        cur = el.get('currency')
        if cur not in curr:
            continue
        buy = float(el.get('saleRate', 0))
        sale = float(el.get('purchaseRate', 0))
        if (buy > 0) and (sale > 0):
            res.append((cur, f"{buy:6.2f}", f"{sale:6.2f}"))
    return res


async def print_data(rates):
    for k, v in rates.items():
        print(f"date: {k}")
        pattern = '|' + Fore.LIGHTGREEN_EX + '{:^10}' + Fore.RESET + '|' + Fore.LIGHTRED_EX + '{:^10}' + \
        Fore.RESET + '|' + Fore.LIGHTYELLOW_EX + '{:^10}' + Fore.RESET  + '|' 
        print(pattern.format('currency', 'sale', 'buy'))
        for el in v:
            print(pattern.format(el[0], el[1], el[2]))
    print()


async def get_date_rate(date):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}') as response:
            print(f"\nStatus: {response.status:3}")
            result = await response.json()
            return result


async def main():
    currency = {'USD', 'EUR', 'CHF', 'GBP', 'PLZ', 'SEK', 'CAD', 'XAU'}
    days = 1

    if len(sys.argv) > 1:
        if ('?' in sys.argv[1]) or ('-' in sys.argv[1]):
            help_prn()
        else:
            if sys.argv[1].isdigit():   # first parameter - days - is specifyed
                days = int(sys.argv[1])
                if days < 1:
                    days = 1
                if days > 10:
                    days = 10
                sys.argv.pop(1)
            if len(sys.argv) > 1: 
                currency.clear()
                sys.argv.pop(0)
                for c in sys.argv:
                    currency.add(c.upper())

    today = datetime.now()
    interval = timedelta(days=1)
    rates = {}

    for i in range(days):
        result_date = (today - interval*i).strftime('%d.%m.%Y')
        rate = await get_date_rate(result_date)
        rates[result_date] = await clean_data(rate.get("exchangeRate"), currency)

    await print_data(rates)  



if __name__ == "__main__":

    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    init()

    asyncio.run(main())





