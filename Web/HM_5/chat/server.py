import asyncio
import logging
import websockets
import names
import aiohttp
from aiofile import async_open
import aiopath
import json
import re
from datetime import datetime, timedelta
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
logging.basicConfig(level=logging.INFO)


async def logger(link, err=None):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    path = aiopath.AsyncPath(link)
    if err:
        async with async_open("log.txt", 'a') as afp:
            await afp.write(f"     Error{err}, {path}, {time}\n")
    else:
        async with async_open("log.txt", 'a') as afp:
            await afp.write(f"Date sent correctly, taken from {path} {time}\n")

async def async_generator_rates(rates):
    for i in rates:
        await asyncio.sleep(0.1)
        yield i


async def async_generator_days(days):
    for i in range(days):
        await asyncio.sleep(0.1)
        yield i


async def async_generator_output(result):
    for i in result:
        await asyncio.sleep(0.1)
        yield i


async def get_exchange(message: str):
    message = message.split(" ")
    if len(message) > 1:
        if message[1].isdigit():
            day = int(message[1])
    else: day = 1
    async with aiohttp.ClientSession() as session:
        try:
            all_rates = []
            async for day in async_generator_days(day):
                time = datetime.today() - timedelta(days=day)
                time = time.strftime("%d.%m.%Y")
                link = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={time}'
                async with session.get(link) as response:
                    all_rates.append(await response.json())
        except aiohttp.ClientConnectorError as err:
            await logger(link, err)
            return "Something went wrong"
        result = []
        async for exchange_per_day in async_generator_rates(all_rates):
            usd = list(filter(lambda el: el["currency"] == "USD", exchange_per_day["exchangeRate"]))
            eur = list(filter(lambda el: el["currency"] == "EUR", exchange_per_day["exchangeRate"]))
            result.append({
                exchange_per_day.get("date"): {
                    "USD": {"sale": usd[0]['saleRateNB'], "purchase": usd[0]['purchaseRateNB']},
                    "EUR": {"sale": eur[0]['saleRateNB'], "purchase": eur[0]['purchaseRateNB']}
                }
            })
        result = json.dumps(result, indent=4)
        await logger(link)
        return result


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            match = re.search(r"exchange\s*(\d+)?", message)
            if match:
                await self.send_to_clients("Need some time")
                exc_rates = await get_exchange(match.group(0))
                await self.send_to_clients(exc_rates)
            else:
                await self.send_to_clients(f"{ws.name}: {message}")


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())