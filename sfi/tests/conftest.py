import pytest
from sfi.server import app_factory
import json

@pytest.fixture
def app():
    app = app_factory(config_param='sfi.server.config.TestingConfig')

    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class Auth:
    def __init__(self, client):
        self._client = client

    def login_researcher(self, email='researcher@sfi.com', password='hashed'):
        return self._client.post(
            '/login_user',
            data=json.dumps({
                'email': email,
                'password': password
            }),
            content_type='application/json')

    def login_admin(self):
        return self.login_researcher(email='admin@sfi.com')

    def logout(self):
        return self._client.get('/api/logout')

@pytest.fixture
def auth(client):
    return Auth(client)
