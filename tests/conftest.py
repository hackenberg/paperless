import os
import tempfile

import pytest

from paperless import create_app
from paperless.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as fd:
    data_sql = fd.read().decode('UTF-8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions:

    def __init__(self, client):
        self.client = client

    def login(self, username='test', password='test'):
        data = {'username': username, 'password': password}
        return self.client.post('/auth/login', data)

    def logout(self):
        return self.client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
