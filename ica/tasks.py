import os
import urllib.parse as urlparse

from redis import Redis
from rq import Queue

redis_url = os.getenv('BROKER_URL')
if not redis_url:
    raise RuntimeError('Redis task queue unavailable')

urlparse.uses_netloc.append('redis')
url = urlparse.urlparse(redis_url)

broker = Redis(host=url.hostname, port=url.port)

high_queue = Queue('high', connection=broker)
default_queue = Queue('default', connection=broker)
low_queue = Queue('low', connection=broker)
