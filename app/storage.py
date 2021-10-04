#!/usr/bin/env python
import abc
import json

import redis
import fakeredis

from models import User


class Storage(abc.ABC):
    """Abstract storage implementation."""

    @abc.abstractmethod
    def save(self, user: User):
        """Persist a User object."""
        pass

    @abc.abstractmethod
    def get(self, username: str) -> User:
        """Retrieve a User object."""
        pass


class RedisStorage(Storage):
    """Implementation of the Redis Storage."""

    def __init__(self, host, port=6379, db=0):
        self._host = host
        self._port = port
        self._db = db
        self._con = None

    @property
    def con(self):
        if self._con is None:
            self._con = redis.Redis(host=self._host, port=self._port, db=self._db)
            self._con.ping()
        return self._con

    def save(self, user: User):
        self.con.set(user.username, json.dumps(user.dict(), default=str))

    def get(self, username: str) -> User:
        raw_data = self.con.get(username)
        if raw_data is None:
            raise Exception("User Not Found")
        user = User(**json.loads(raw_data))
        return user


class FakeRedisStorage(RedisStorage):
    """Implementation of the Redis Storage."""

    def __init__(self, host, port=6379, db=0, server=None):
        super().__init__(host, port, db)
        self._server = server if server is not None else fakeredis.FakeServer()

    @property
    def con(self):
        if self._con is None:
            self._con = fakeredis.FakeRedis(server=self._server)
            self._con.ping()
        return self._con


class DynamoDBStorage(Storage):
    """NOTE(mmicu): to implement"""

    pass


class CloudFireStoreStorage(Storage):
    """NOTE(mmicu): to implement"""

    pass
