import pickle

import aioredis


class Storage:
    @classmethod
    async def create_storage(cls):
        raise NotImplemented("Storage not implemented")

    async def close(self):
        raise NotImplemented("Storage not implemented")

    async def get_by_key(self, key):
        raise NotImplemented("Storage not implemented")


class RedisStorage(Storage):
    @classmethod
    async def create_storage(cls, redis_dsn):
        redis = aioredis.from_url(redis_dsn, decode_responses=True)
        return cls(redis)

    def __init__(self, redis):
        self.redis = redis

    async def close(self):
        await self.redis.close()

    async def get_by_key(self, key):
        value = await self.redis.get(key)
        return pickle.loads(value)

    async def set_by_key(self, key, value):
        value = pickle.dumps(value)
        await self.redis.set(key, value)
