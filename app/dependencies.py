#!/usr/bin/env python
import os
from flask import Config


from injector import singleton

import storage
import message


def configure(binder):
    """Configure dependency injections"""
    binder.bind(
        storage.Storage,
        # NOTE(mmicu): here we should probably implement a config module to
        # have one place where we define config variables, there default
        # and how to parse them
        to=storage.RedisStorage(
            host=os.getenv("REDIS_HOST"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=int(os.getenv("REDIS_DB", 0)),
        ),
        scope=singleton,
    )
