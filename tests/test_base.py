import pytest


@pytest.mark.parametrize(('included', 'excluded'), (
    (b'jquery.js', b'jquery.min.js'),
    (b'bootstrap.js', b'bootstrap.min.js'),
    (b'bootstrap.css', b'bootstrap.min.css'),
))
def test_config_env(client, included, excluded):
    url = '/docs/'
    response = client.get(url)
    assert response.status_code == 200
    assert included in response.data
    assert excluded not in response.data
