import pytest
from rest_framework.test import APIClient

from tests.factories import ProfileFactory, UserFactory


@pytest.fixture(autouse=True)
def autouse_db(db):
    pass


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def profile():
    return ProfileFactory()
