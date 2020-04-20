import re
from datetime import datetime
from urllib import parse

from flask import Flask
from flask import request, jsonify, make_response
from flask_redis import Redis

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
redis = Redis(app)


@app.route('/visited_links', methods=['POST'])
def visited_links():
    if not request.json or 'links' not in request.json:
        return jsonify({'status': 'error: Bad Request'}), 400

    for link in request.json['links']:
        timestamp = int(datetime.timestamp(datetime.now()))
        url = parse.urlparse(link if re.match(r'https?://', link) else f'http://{link}')
        redis.sadd(timestamp, url.hostname)
    return jsonify({'status': 'ok'}), 201


@app.route('/visited_domains', methods=['GET'])
def visited_domains():
    if not request.args or not {'from', 'to'} == set(request.args):
        return jsonify({'status': 'error: Bad Request'}), 400

    request_from = int(request.args.get('from'))
    request_to = int(request.args.get('to'))
    domains = set()
    for item in redis.keys('*'):
        if int(item) in range(request_from, request_to):
            domains |= redis.smembers(item)
    response = {'domains': list(domains), 'status': 'ok'}
    return jsonify(response)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'status': f'error: {error}'}), 404)


@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify({'status': f'error: {error}'}), 405)


@app.errorhandler(500)
def internal_error(error):
    return make_response(jsonify({'status': f'error: {error}'}), 500)


if __name__ == '__main__':
    app.run()
