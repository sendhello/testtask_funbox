from datetime import datetime

import pytest
from flask import url_for


@pytest.mark.options(debug=False)
def test_app(app):
    assert not app.debug, 'Ensure the app not in debug mode'


def test_visited_links(client):
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


def test_visited_domains(client):
    timestamp_to = int(datetime.timestamp(datetime.now()))
    timestamp_from = timestamp_to - 60
    url = f'{url_for("visited_domains")}?&from={timestamp_from}&to={timestamp_to}'
    response = client.get(url)
    assert response.status_code == 200
    assert set(response.json.get('domains')) == {'stackoverflow.ru', 'ya.ru', 'funbox.ru'}
    assert response.json.get('status') == 'ok'
