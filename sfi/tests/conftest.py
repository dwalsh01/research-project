import pytest
from sfi.server import app_factory


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
