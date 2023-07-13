import os

import jsonpickle
import redis.asyncio as redis

from custom_emoji_app.repositories.redis.Irepo import IRedisRepo


class RedisRepo(IRedisRepo):
    def __init__(self):
        # read redis configuration parameter from env
        self.connection_parameter = {
            "host": os.getenv("REDIS_HOST"),
            "port": os.getenv("REDIS_PORT"),
            "password": os.getenv("REDIS_PASS"),
            "ssl": True if os.getenv("REDIS_SSL_ENABLED") == "ON" else False,
            "db": 0}

    def __get_connection(self):
            return redis.Redis(**self.connection_parameter)
    async def get_cache(self, key):
        connection = self.__get_connection()
        res = await connection.get(key)
        await connection.close()
        return res

    async def get_all_cache(self):
        connection = self.__get_connection()
        res = dict()
        async for key in connection.scan_iter():
            decoded_key = key.decode("utf-8")
            val = await connection.get(key)
            res[decoded_key] = val.decode("utf-8")
        return res

    async def set_cache(self, key, value):
        print("start storing cache")
        connection = self.__get_connection()
        await connection.set(key, jsonpickle.encode(value))
        await connection.close()

    async def delete_cache_with_key(self, key):
        connection = self.__get_connection()
        await connection.delete(key)
        await connection.close()

    async def delete_cache_with_prefix(self, prefix):
        connection = self.__get_connection()
        keys_with_prefix = connection.scan_iter(match=prefix + "_*")
        async for key in keys_with_prefix:
            await connection.delete(key)
        await connection.close()

    async def delete_all_cache(self):
        connection = self.__get_connection()
        async for key in connection.scan_iter():
            await connection.delete(key)
        await connection.close()

    async def health_check(self) -> bool:
        connection = self.__get_connection()
        try:
            await connection.ping()
        except (redis.ConnectionError, ConnectionRefusedError):
            return False
        await connection.close()
        return True