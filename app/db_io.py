import re
from datetime import datetime
from urllib import parse

from . import redis, app


def get_prefix():
    return f'{app.config["KEY_PREFIX"]}:' if app.config.get("KEY_PREFIX") else ''


def db_write(link):
    prefix = get_prefix()
    timestamp = int(datetime.timestamp(datetime.now()))
    url = parse.urlparse(link if re.match(r'https?://', link) else f'http://{link}')
    redis.sadd(f'{prefix}{timestamp}', url.hostname)


def db_read(request):
    prefix = get_prefix()
    timestamp_from = request.args.get('from')
    timestamp_to = request.args.get('to')
    domains = set()
    for item in redis.keys(f'{prefix}*'):
        if int(item.split(':')[1]) in range(int(timestamp_from), int(timestamp_to)):
            domains |= redis.smembers(item)
    response = {'domains': list(domains), 'status': 'ok'}
    return response
