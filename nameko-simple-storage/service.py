# coding: utf-8

import pickle
from hashlib import sha256
from uuid import uuid4
from typing import List

from dependencies import Redis
from nameko.rpc import rpc
from nameko.timer import timer
from redis import StrictRedis
from redis.exceptions import ConnectionError, AuthenticationError, TimeoutError

from exceptions import SimpleStorageError, SimpleStorageNotFoundError


class SimpleStorage(object):

    name = 'simple_storage'

    # Dependency injection
    redis: StrictRedis = Redis()

    @rpc
    def get_item(self, key: str, delete_after_read: bool=False) -> tuple:
        """
        Returns data stored in Redis related to the given key
        :param key: (str) the redis key
        :param delete_after_read: (bool) if True delete data after reading
        :return: (tuple) returns data, metadata
        :exception SimpleStorageError, SimpleStorageNotFoundError
        """
        try:
            if self.redis.exists(name=key):
                data, metadata = self.redis.hmget(name=key,
                                                  keys=['data',
                                                        'metadata'])
                if delete_after_read:
                    self.redis.delete(key)
                return pickle.loads(data), pickle.loads(metadata)
            else:
                raise SimpleStorageNotFoundError(f'Can\'t find key {key}')

        except (AuthenticationError, ConnectionError, TimeoutError) as err:
            raise SimpleStorageError(f'Problem with the Redis server ({err})')

    @rpc
    def list_items(self) -> List[str]:
        """
        List all the keys stored in the Redis DB
        :return: (list) list of keys
        :exception SimpleStorageError
        """
        keys = []
        try:
            if self.redis.keys():
                keys = [key.decode(encoding='utf-8') for key in self.redis.keys()]

        except (AuthenticationError, ConnectionError, TimeoutError) as err:
            raise SimpleStorageError(f'Problem with the Redis server ({err})')
        else:
            return keys

    @rpc
    def put_item(self, data, expiration: int=None, **kwargs) -> str:
        """
        Store the given data (and optionally metadata) to Redis DB
        :param data: the data to store
        :param expiration: (int) number of seconds before data expires (default: None)
        :param kwargs: kwargs used as metadata
        :return: SimpleStorageError
        """
        # First, we use pickle to serialize the data
        data_dumped = pickle.dumps(data)
        metadata_dumped = pickle.dumps(kwargs)

        # Then, we generate a unique key by hashing data (salted with an UUID
        # to avoid collision if you're using exactly the same data + metadata)
        uuid = pickle.dumps(uuid4())
        redis_key = sha256(data_dumped+metadata_dumped+uuid).hexdigest()

        try:
            self.redis.hmset(redis_key, {'data': data_dumped,
                                         'metadata': metadata_dumped})

            if expiration:
                self.redis.expire(redis_key, expiration)

        except (AuthenticationError, ConnectionError, TimeoutError) as err:
            raise SimpleStorageError(f'Problem with the Redis server ({err})')
        else:
            return redis_key

    @rpc
    @timer(interval=300)
    def save_db(self) -> None:
        """
        Save the Redis database every 5 minutes
        :return: None
        :exception SimpleStorageError
        """
        try:
            self.redis.save()
        except (AuthenticationError, ConnectionError, TimeoutError) as err:
            raise SimpleStorageError(f'Problem with the Redis server ({err})')
