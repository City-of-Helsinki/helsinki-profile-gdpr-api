import requests_mock
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from tests.conftest import get_api_token_for_user_with_scopes

User = get_user_model()


def do_query(user, id_value, scopes=(settings.GDPR_API_QUERY_SCOPE,)):
    api_client = APIClient()

    with requests_mock.Mocker() as req_mock:
        auth_header = get_api_token_for_user_with_scopes(user, scopes, req_mock)
        api_client.credentials(HTTP_AUTHORIZATION=auth_header)

        return api_client.get(reverse("helsinki_gdpr:gdpr_v1", kwargs={"pk": id_value}))


def test_get_profile_information_from_gdpr_api(profile, snapshot):
    response = do_query(profile.user, profile.id)

    assert response.status_code == 200
    snapshot.assert_match(response.json())


def test_gdpr_api_requires_authentication(api_client, profile):
    response = api_client.get(
        reverse("helsinki_gdpr:gdpr_v1", kwargs={"pk": profile.id})
    )
    assert response.status_code == 401


def test_user_can_only_access_his_own_profile(user, profile):
    response = do_query(user, profile.id)

    assert response.status_code == 403


def test_gdpr_query_requires_correct_query_scope(profile, settings):
    response = do_query(
        profile.user, profile.id, scopes=[settings.GDPR_API_DELETE_SCOPE]
    )

    assert response.status_code == 403


def test_if_profile_not_found_return_204(user, uuid_value):
    response = do_query(user, uuid_value)

    assert response.status_code == 204


def test_model_lookup_can_be_configured_to_a_field(profile, snapshot, settings):
    settings.GDPR_API_MODEL_LOOKUP = "user__uuid"

    response = do_query(profile.user, profile.user.uuid)

    assert response.status_code == 200
    snapshot.assert_match(response.json())
