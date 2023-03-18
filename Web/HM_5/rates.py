import argparse
import platform
import aiohttp
import asyncio
import json
from datetime import datetime, timedelta

parser = argparse.ArgumentParser(description='day, exchange rate')
parser.add_argument('--days', "-d", default=1, type=int)
parser.add_argument('--list', '-l', help='delimited list input', default="EUR, USD", type=str)
args = vars(parser.parse_args())
days_to_subtract = args.get('days')
exc_rates = args.get('list').strip()
exc_rates = exc_rates.split(",")

# how the command should look like: py .\rates.py -d 4 -l "GEL,USD,EUR"
#
# possible rates: "AZN", "BYN", "CAD", "CHF", "CNY", "CZK", "DKK", "GBP", "GEL", "HUF", "ILS", "JPY", "KZT",
#                 "MDL", "NOK", "PLN", "SEK", "SGD", "TMT","TRY", "USD", "UZS", "XAU"


async def async_generator_days(days):
    for i in range(days):
        await asyncio.sleep(0.1)
        yield i


async def async_generator_rates(rates):
    for i in rates:
        await asyncio.sleep(0.1)
        yield i


async def async_generator_exc_rates(rates):
    for i in rates:
        await asyncio.sleep(0.1)
        yield i


async def main():
    if days_to_subtract < 0:
        return "Value is wrong (should be > 0)"
    async with aiohttp.ClientSession() as session:
        try:
            all_rates = []
            async for day in async_generator_days(days_to_subtract):
                time = datetime.today() - timedelta(days=day)
                time = time.strftime("%d.%m.%Y")
                link = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={time}'
                async with session.get(link) as response:
                    all_rates.append(await response.json())
        except aiohttp.ClientConnectorError as err:
            return f'Connection error: {str(err)}'
        result = []
        async for exchange_per_day in async_generator_rates(all_rates):
            date = exchange_per_day["date"]
            rate_per_day = {date: []}
            async for rate in async_generator_exc_rates(exc_rates):
                user_rate = list(filter(lambda el: el["currency"] == rate, exchange_per_day["exchangeRate"]))
                rate_per_day[date].append({rate: {"sale": user_rate[0]['saleRateNB'], "purchase": user_rate[0]['purchaseRateNB']}})
            result.append(rate_per_day)
        result = json.dumps(result, indent=2)
        return result


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
    print(r)
