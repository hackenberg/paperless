import pytest

from flask import g, session

from paperless.db import get_db


def test_index(client, app):
    url = '/search/'
    data = {'search': 'expr'}
    assert client.get(url).status_code == 200
    response = client.post(url, data=data)
    assert response.status_code == 200


@pytest.mark.parametrize(('search', 'message'), (
    ('', b'Expression is required.'),
))
def test_index_validate_input(client, search, message):
    data = {'search': search}
    response = client.post('/search/', data=data)
    assert message in response.data
