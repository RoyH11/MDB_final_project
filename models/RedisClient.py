from redis import Redis

class RedisClient:
    def __init__(self, port=6379):
        self.redisClient = Redis(port=port)

    def close(self):
        self.redisClient.close()