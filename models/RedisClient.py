import redis

class RedisClient:
    def __init__(self, port=6379):
        self.redisClient = redis.Redis(port=port)

    def close(self):
        self.redisClient.close()