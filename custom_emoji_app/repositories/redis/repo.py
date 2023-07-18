import os
from typing import Any

import jsonpickle
import redis
from dotenv import load_dotenv

load_dotenv()


class RedisRepository:
    def __init__(self):
        # read redis configuration parameter from env
        self.connection_parameter = {
            "host": os.getenv('REDIS_HOST'),
            "port": os.getenv('REDIS_PORT'),
            "db": os.getenv('REDIS_DB')}
        self.client = redis.Redis(**self.connection_parameter)

    def get_data_by_key(self, key: str):
        res = self.client.get(key)
        if res:
            return res.decode('utf-8')
        raise ValueError(f'No value found by the key {key}')

    def get_all_data(self):
        res = dict()
        for key in self.client.scan_iter():
            decoded_key = key.decode("utf-8")
            val = self.client.get(key)
            res[decoded_key] = val.decode("utf-8")
        return res

    def set_data(self, key: str, value: Any):
        self.client.set(key, jsonpickle.encode(value))

    def delete_data_by_key(self, key: str):
        self.client.delete(key)

    def delete_cache_with_prefix(self, prefix: str):
        keys_with_prefix = self.client.scan_iter(match=prefix + "_*")
        for key in keys_with_prefix:
            self.client.delete(key)

    def delete_all_cache(self):
        for key in self.client.scan_iter():
            self.client.delete(key)

    def health_check(self) -> bool:
        try:
            self.client.ping()
        except (redis.ConnectionError, redis.ConnectionRefusedError):
            return False
        return True