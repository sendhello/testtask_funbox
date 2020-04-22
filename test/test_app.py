import re
from datetime import datetime

from flask import url_for


def test_visited_links_1(client):
    data = """
        {
            "links": [
                "https://ya.ru",
                "https://ya.ru?q=123",
                "funbox.ru",
                "https://stackoverflow.ru/questions/11828270/how-to-exit-the-vim-editor"
            ]
        }
        """
    response = client.post(url_for('visited_links'), content_type='application/json', data=data)
    assert response.status_code == 201
    assert response.json == {'status': 'ok'}


def test_visited_links_2(client):
    data = """
        {
            "urls": [
                "https://ya.ru",
                "https://ya.ru?q=123",
                "funbox.ru",
                "https://stackoverflow.ru/questions/11828270/how-to-exit-the-vim-editor"
            ]
        }
        """
    response = client.post(url_for('visited_links'), content_type='application/json', data=data)
    assert response.status_code == 400
    assert response.json.get('status') == 'error: Bad Request'


def test_visited_links_3(client):
    response = client.get(url_for('visited_links'))
    assert response.status_code == 405
    assert re.match(r'error:', response.json.get('status'))


def test_visited_domains_1(client):
    timestamp_to = int(datetime.timestamp(datetime.now())) + 5
    timestamp_from = timestamp_to - 10
    url = f'{url_for("visited_domains")}?&from={timestamp_from}&to={timestamp_to}'
    response = client.get(url)
    assert response.status_code == 200
    assert set(response.json.get('domains')) == {'stackoverflow.ru', 'ya.ru', 'funbox.ru'}
    assert response.json.get('status') == 'ok'


def test_visited_domains_2(client):
    timestamp_to = int(datetime.timestamp(datetime.now())) + 5
    url = f'{url_for("visited_domains")}?&to={timestamp_to}'
    response = client.get(url)
    assert response.status_code == 400
    assert response.json.get('status') == 'error: Bad Request'


def test_visited_domains_3(client):
    response = client.get(url_for("visited_domains"))
    assert response.status_code == 400
    assert response.json.get('status') == 'error: Bad Request'
