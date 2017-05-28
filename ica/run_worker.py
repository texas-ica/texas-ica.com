import os
import urllib.parse as urlparse

from redis import Redis
from rq import Queue, Connection

config = os.getenv('CONFIG')

if 'Testing' in config:
    from rq.worker import Worker
else:
    from rq.worker import HerokuWorker as Worker

listen = ['high', 'default', 'low']

redis_url = os.getenv('BROKER_URL')
if not redis_url:
    raise RuntimeError('Redis task queue unavailable')

urlparse.uses_netloc.append('redis')
url = urlparse.urlparse(redis_url)

conn = Redis(host=url.hostname, port=url.port, db=0)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
