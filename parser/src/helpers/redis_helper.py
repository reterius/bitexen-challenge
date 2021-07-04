import datetime

import redis


class RedisHelper:

    def __init__(self, host_dsn: str, host_port: int, db: int, password: str = None):
        self.host_dsn = host_dsn
        self.host_port = host_port
        self.db = db
        # self.client = redis.StrictRedis(host=self.host_dsn, port=self.host_port, db=self.db)
        self.pool = redis.ConnectionPool(host=self.host_dsn, port=self.host_port, db=self.db, password=password)
        self.client = redis.Redis(connection_pool=self.pool, password=password)

    def set(self, key: str, value: str):
        self.client.set(key, value)

    def get(self, key: str):
        return self.client.get(key)

    def remove(self, key: str):
        self.client.delete(key)

    def set_with_expire(self, key: str, value: str, expire_time_sec: int, expire_callback):
        self.client.set_response_callback('EXPIRE', callback=expire_callback)
        self.client.set(key, value)
        self.client.expire(key, expire_time_sec)

        '''
        ttl = datetime.today() + timedelta(hours=72)  
        r.hset(name=name, key=hash_key, value=hash_data)  
        r.expire(name=hash_name, time=ttl)
        '''

    def exist(self, key: str):
        return self.client.exists(key)
