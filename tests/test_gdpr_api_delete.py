import urllib
from typing import Optional

import pytest
import requests_mock
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from helsinki_gdpr.types import Error, ErrorResponse
from tests.conftest import get_api_token_for_user_with_scopes
from tests.factories import ExtraDataFactory

from .models import Profile

User = get_user_model()


def do_delete(
    user,
    id_value,
    scopes=(settings.GDPR_API_DELETE_SCOPE,),
    query_params=None,
    data=None,
    url_id_param_name="pk",
):
    api_client = APIClient()

    with requests_mock.Mocker() as req_mock:
        auth_header = get_api_token_for_user_with_scopes(user, scopes, req_mock)
        api_client.credentials(HTTP_AUTHORIZATION=auth_header)

        if query_params:
            query = "?" + urllib.parse.urlencode(query_params)
        else:
            query = ""

        request_kwargs = {"format": "json"}
        if data:
            request_kwargs["data"] = data

        return api_client.delete(
            reverse("helsinki_gdpr:gdpr_v1", kwargs={url_id_param_name: id_value})
            + query,
            **request_kwargs,
        )


def test_delete_profile_dry_run_data(true_value, profile):
    response = do_delete(profile.user, profile.id, data={"dry_run": true_value})

    assert response.status_code == 204
    assert Profile.objects.count() == 1
    assert User.objects.count() == 1


def test_delete_profile_dry_run_query_params(true_value, profile):
    response = do_delete(profile.user, profile.id, query_params={"dry_run": true_value})

    assert response.status_code == 204
    assert Profile.objects.count() == 1
    assert User.objects.count() == 1


def test_delete_profile(profile):
    response = do_delete(profile.user, profile.id)

    assert response.status_code == 204
    assert Profile.objects.count() == 0
    assert User.objects.count() == 0


def test_delete_profile_dry_run_query_params_false(false_value, profile):
    response = do_delete(
        profile.user, profile.id, query_params={"dry_run": false_value}
    )

    assert response.status_code == 204
    assert Profile.objects.count() == 0
    assert User.objects.count() == 0


def test_delete_profile_dry_run_data_false(false_value, profile):
    response = do_delete(profile.user, profile.id, data={"dry_run": false_value})

    assert response.status_code == 204
    assert Profile.objects.count() == 0
    assert User.objects.count() == 0


def test_deletion_forbidden(profile):
    profile.memo = "nodelete"
    profile.save()

    response = do_delete(profile.user, profile.id)

    assert response.status_code == 403
    assert len(response.content) == 0
    assert Profile.objects.count() == 1
    assert User.objects.count() == 1


def test_gdpr_api_requires_authentication(api_client, profile):
    response = api_client.delete(
        reverse("helsinki_gdpr:gdpr_v1", kwargs={"pk": profile.id})
    )
    assert response.status_code == 401


def test_user_can_only_access_his_own_profile(user, profile):
    response = do_delete(user, profile.id)

    assert response.status_code == 403


def test_gdpr_delete_requires_correct_delete_scope(profile, settings):
    response = do_delete(
        profile.user, profile.id, scopes=[settings.GDPR_API_QUERY_SCOPE]
    )

    assert response.status_code == 403
    assert Profile.objects.count() == 1
    assert User.objects.count() == 1


def test_if_profile_not_found_return_204(user, uuid_value):
    response = do_delete(user, uuid_value)

    assert response.status_code == 204


def test_model_lookup_can_be_configured_to_a_field(profile, settings):
    settings.GDPR_API_MODEL_LOOKUP = "user__uuid"

    response = do_delete(profile.user, profile.user.uuid)

    assert response.status_code == 204
    assert Profile.objects.count() == 0
    assert User.objects.count() == 0


@pytest.mark.parametrize("finds_instance", (True, False))
@pytest.mark.parametrize(
    "lookup_function",
    ("model_lookup_that_returns_none", "model_lookup_that_throws_exception"),
)
def test_model_lookup_can_be_configured_to_a_function(
    finds_instance,
    lookup_function,
    uuid_value,
    profile,
    settings,
):
    settings.GDPR_API_MODEL_LOOKUP = f"tests.conftest.{lookup_function}"

    instance_id = profile.user.uuid if finds_instance else uuid_value
    response = do_delete(profile.user, instance_id)

    assert response.status_code == 204

    if finds_instance:
        assert Profile.objects.count() == 0
        assert User.objects.count() == 0
    else:
        assert Profile.objects.count() == 1
        assert User.objects.count() == 1


def test_user_provider_function_can_be_configured(profile, settings):
    ExtraDataFactory(profile=profile)

    settings.GDPR_API_MODEL = "tests.ExtraData"
    settings.GDPR_API_MODEL_LOOKUP = "profile__id"
    settings.GDPR_API_USER_PROVIDER = "tests.conftest.get_user_from_extra_data"

    response = do_delete(profile.user, profile.id)

    assert response.status_code == 204
    assert Profile.objects.count() == 0
    assert User.objects.count() == 0


def anonymising_deleter(profile, is_dry_run):
    profile.memo = "anonymised"
    profile.save()


def test_deleter_function_can_be_configured(profile, settings):
    settings.GDPR_API_DELETER = "tests.test_gdpr_api_delete.anonymising_deleter"

    response = do_delete(profile.user, profile.id)

    assert response.status_code == 204
    profile = Profile.objects.get()
    assert profile.memo == "anonymised"
    assert User.objects.count() == 1


def error_returning_deleter(profile, is_dry_run) -> Optional[ErrorResponse]:
    return ErrorResponse(
        [Error("NO_GO", {"en": "Can't do", "fi": "Ei pysty", "sv": "Kan inte"})]
    )


def test_deleter_function_can_provide_errors(profile, settings, snapshot):
    settings.GDPR_API_DELETER = "tests.test_gdpr_api_delete.error_returning_deleter"

    response = do_delete(profile.user, profile.id)

    assert response.status_code == 403
    assert Profile.objects.count() == 1
    assert User.objects.count() == 1

    assert response["Content-Type"] == "application/json"
    snapshot.assert_match(response.json())


def nonsense_returning_deleter(profile, is_dry_run):
    return False


def test_deleter_function_can_not_return_nonsense(profile, settings, snapshot):
    settings.GDPR_API_DELETER = "tests.test_gdpr_api_delete.nonsense_returning_deleter"

    response = do_delete(profile.user, profile.id)

    assert response.status_code == 403
    assert Profile.objects.count() == 1
    assert User.objects.count() == 1

    assert response["Content-Type"] == "application/json"
    snapshot.assert_match(response.json())


def test_gdpr_url_pattern_can_be_configured(profile, settings):
    settings.GDPR_API_URL_PATTERN = "my/own/<uuid:my_id>/pattern"

    response = do_delete(profile.user, profile.id, url_id_param_name="my_id")

    assert response.status_code == 204
    assert Profile.objects.count() == 0
    assert User.objects.count() == 0
