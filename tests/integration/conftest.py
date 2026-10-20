import os

import pytest
from sqlalchemy.engine import make_url

from app import create_app
from app.extensions import db


@pytest.fixture(scope="session")
def integration_app():
    database_url = os.environ.get("TEST_DATABASE_URL")

    if not database_url:
        pytest.fail("Set TEST_DATABASE_URL before running integration tests.")

    url = make_url(database_url)

    if url.database != "taskflow_test":
        pytest.fail(
            "Integration tests may only use the taskflow_test database."
        )

    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "integration-test-secret",
            "SQLALCHEMY_DATABASE_URI": database_url,
        }
    )

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()


@pytest.fixture
def postgres_app(integration_app):
    with integration_app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()

    yield integration_app

    with integration_app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def postgres_client(postgres_app):
    return postgres_app.test_client()
