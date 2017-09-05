import os

import redis
from rq.job import Job

r = redis.StrictRedis(
    host='redis-16296.c10.us-east-1-4.ec2.cloud.redislabs.com',
    port=16296
)

job_ids = [o.decode('utf-8')[7:] for o in r.keys('rq:job*')]
for job_id in job_ids:
    job = Job.fetch(job_id, connection=r)
    if job.get_status() in set(['failed', 'finished']):
        print('Deleting {}'.format(job_id))
        job.delete()

print('Number of keys: {}'.format(r.dbsize()))
