import redis
from django.conf import settings
import json
from djangocrawler.logger import log


class QueueServer(object):
    shared_state = {}

    def __init__(self):
        self.__dict__ = self.shared_state

    def redis_connect(self):
        connection_pool = redis.ConnectionPool(host=settings.HOST, port=settings.PORT, password =settings.PASSWORD,db=0)
        return redis.StrictRedis(connection_pool=connection_pool)

    def publish(self,data):
        """

        :param data:
        :return:
        """
        try:
            redis_conn = self.redis_connect()
            channel = redis_conn.pubsub()
            redis_conn.publish(settings.CHANNEL, json.dumps(data))
        except Exception as e:
            log.exception (e.__str__())
