import os
from typing import Generator
from contextlib import contextmanager
from redis import Redis

@contextmanager
def get_redis_client_generator() -> Generator[Redis, None, None]:
    client: Redis = Redis(host=os.getenv("REDIS_HOST"), 
                          port=os.getenv("REDIS_PORT"), 
                          db=0
                        )
    try:
        yield client
    finally:
        client.connection_pool.disconnect()

def get_redis_client() -> Redis:
    with get_redis_client_generator() as client:
        return client