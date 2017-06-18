import os
import redis

REDIS_PORT = 6379
REDIS_DB = 0
REDIS_HOST = os.environ.get('REDIS_PORT_6379_TCP_ADDR', 'redis')

REDIS_CONNECTION_POOL = redis.ConnectionPool(host=REDIS_HOST,
                                             port=REDIS_PORT,
                                             db=REDIS_DB)
