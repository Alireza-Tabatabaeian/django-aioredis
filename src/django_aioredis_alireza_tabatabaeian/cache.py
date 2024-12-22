import aioredis
from django.core.cache.backends.base import BaseCache, DEFAULT_TIMEOUT
from asgiref.sync import async_to_sync

class AsyncRedisCache(BaseCache):
    def __init__(self, location, params):
        super().__init__(params)
        self._redis_url = location
        self._client = None

    async def get_client(self):
        if not self._client:
            self._client = await aioredis.from_url(self._redis_url)
        return self._client

    async def aget(self, key,default=None,version=None):
        client = await self.get_client()
        value = await client.get(key)
        return value.decode('utf-8') if value else None

    async def aset(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        client = await self.get_client()
        await client.set(key, value, ex=timeout)

    #
    def get(self, key, default=None, version=None):
        return async_to_sync(self.aget)(key) or default

    def set(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        async_to_sync(self.aset)(key, value, timeout)