from flask import request, jsonify, make_response

from . import app
from .db_io import db_write, db_read


@app.route('/visited_links', methods=['POST'])
def visited_links():
    if not request.json or 'links' not in request.json:
        return jsonify({'status': 'error: Bad Request'}), 400

    for link in request.json['links']:
        db_write(link)
    return jsonify({'status': 'ok'}), 201


@app.route('/visited_domains', methods=['GET'])
def visited_domains():
    if not request.args or not {'from', 'to'} == set(request.args):
        return jsonify({'status': 'error: Bad Request'}), 400

    response = db_read(request)
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
