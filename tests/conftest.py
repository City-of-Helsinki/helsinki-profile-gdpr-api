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


@pytest.fixture(params=["true", "True", "TRUE", "1", 1, True])
def true_value(request):
    return request.param


@pytest.fixture(params=["false", "False", "FALSE", "0", 0, False])
def false_value(request):
    return request.param
