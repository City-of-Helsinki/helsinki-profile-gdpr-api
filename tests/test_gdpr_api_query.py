import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from tests.conftest import get_api_token_for_user_with_scopes

User = get_user_model()


def test_get_profile_information_from_gdpr_api(
    api_client, profile, snapshot, requests_mock, settings
):
    profile.user.first_name = "First"
    profile.user.save()
    auth_header = get_api_token_for_user_with_scopes(
        profile.user, [settings.GDPR_API_QUERY_SCOPE], requests_mock
    )
    api_client.credentials(HTTP_AUTHORIZATION=auth_header)
    response = api_client.get(
        reverse("helsinki_gdpr:gdpr_v1", kwargs={"pk": profile.id})
    )

    assert response.status_code == 200
    snapshot.assert_match(response.json())


def test_gdpr_api_requires_authentication(api_client, profile):
    response = api_client.get(
        reverse("helsinki_gdpr:gdpr_v1", kwargs={"pk": profile.id})
    )
    assert response.status_code == 401


def test_user_can_only_access_his_own_profile(
    api_client, user, profile, requests_mock, settings
):
    auth_header = get_api_token_for_user_with_scopes(
        user,
        [settings.GDPR_API_QUERY_SCOPE, settings.GDPR_API_DELETE_SCOPE],
        requests_mock,
    )
    api_client.credentials(HTTP_AUTHORIZATION=auth_header)

    response = api_client.get(
        reverse("helsinki_gdpr:gdpr_v1", kwargs={"pk": profile.id})
    )
    assert response.status_code == 403


@pytest.mark.parametrize("use_correct_scope", [True, False])
def test_gdpr_query_requires_correct_scope(
    use_correct_scope, api_client, profile, requests_mock, settings
):
    if use_correct_scope:
        auth_header = get_api_token_for_user_with_scopes(
            profile.user,
            [settings.GDPR_API_QUERY_SCOPE, settings.GDPR_API_DELETE_SCOPE],
            requests_mock,
        )
    else:
        auth_header = get_api_token_for_user_with_scopes(
            profile.user, [settings.GDPR_API_DELETE_SCOPE], requests_mock
        )
    api_client.credentials(HTTP_AUTHORIZATION=auth_header)

    response = api_client.get(
        reverse("helsinki_gdpr:gdpr_v1", kwargs={"pk": profile.id})
    )

    if use_correct_scope:
        assert response.status_code == 200
    else:
        assert response.status_code == 403
