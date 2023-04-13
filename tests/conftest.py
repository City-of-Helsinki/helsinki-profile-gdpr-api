import datetime
import uuid

import pytest
from helusers.settings import api_token_auth_settings
from jose import jwt
from rest_framework.test import APIClient

from tests.factories import ProfileFactory, UserFactory
from tests.keys import rsa_key


@pytest.fixture(autouse=True)
def autouse_db(db):
    pass


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def uuid_value():
    return uuid.uuid4()


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


def get_api_token_for_user_with_scopes(user, scopes: list, requests_mock):
    """Build a proper auth token with desired scopes."""
    audience = api_token_auth_settings.AUDIENCE
    issuer = api_token_auth_settings.ISSUER
    auth_field = api_token_auth_settings.API_AUTHORIZATION_FIELD
    config_url = f"{issuer}/.well-known/openid-configuration"
    jwks_url = f"{issuer}/jwks"

    configuration = {
        "issuer": issuer,
        "jwks_uri": jwks_url,
    }

    keys = {"keys": [rsa_key.public_key_jwk]}

    now = datetime.datetime.now()
    expire = now + datetime.timedelta(days=14)

    jwt_data = {
        "iss": issuer,
        "aud": audience,
        "sub": str(user.uuid),
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        auth_field: scopes,
    }
    encoded_jwt = jwt.encode(
        jwt_data, key=rsa_key.private_key_pem, algorithm=rsa_key.jose_algorithm
    )

    requests_mock.get(config_url, json=configuration)
    requests_mock.get(jwks_url, json=keys)

    auth_header = f"{api_token_auth_settings.AUTH_SCHEME} {encoded_jwt}"

    return auth_header


def model_lookup_that_returns_none(model, instance_id):
    return model.objects.filter(user__uuid=instance_id).first()


def model_lookup_that_throws_exception(model, instance_id):
    return model.objects.get(user__uuid=instance_id)


def get_user_from_extra_data(extra_data):
    return extra_data.profile.user
