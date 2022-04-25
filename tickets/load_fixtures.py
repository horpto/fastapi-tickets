#!/usr/bin/env python3

import asyncio

import yaml

from config import settings
from models import FlightPricesModel
from storage import RedisStorage


async def import_flight_prices(storage):
    with open('./fixtures/prices.yml', 'r') as f:
        for obj in yaml.safe_load(f):
            fpm = FlightPricesModel(storage=storage, **obj)
            # TODO: can be slow if too many objects
            await fpm.save()


async def main():
    storage = await RedisStorage.create_storage(settings.redis_dsn)

    await import_flight_prices(storage)


if __name__ == '__main__':
    asyncio.run(main())
