from app import app as flask_app
import pytest


@pytest.fixture
def app():
    app = flask_app
    return app
