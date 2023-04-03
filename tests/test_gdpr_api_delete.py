import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from tests.conftest import get_api_token_for_user_with_scopes

from .models import Profile

User = get_user_model()


def test_delete_profile_dry_run_data(
    true_value, api_client, profile, requests_mock, settings
):
    auth_header = get_api_token_for_user_with_scopes(
        profile.user, [settings.GDPR_API_DELETE_SCOPE], requests_mock
    )
    api_client.credentials(HTTP_AUTHORIZATION=auth_header)
    response = api_client.delete(
        reverse("helsinki_gdpr:gdpr_v1", kwargs={"pk": profile.id}),
        data={"dry_run": true_value},
        format="json",
    )

    assert response.status_code == 204
    assert Profile.objects.count() == 1
    assert User.objects.count() == 1


def test_delete_profile_dry_run_query_params(
    true_value, api_client, profile, requests_mock, settings
):
    auth_header = get_api_token_for_user_with_scopes(
        profile.user, [settings.GDPR_API_DELETE_SCOPE], requests_mock
    )
    api_client.credentials(HTTP_AUTHORIZATION=auth_header)
    response = api_client.delete(
        reverse("helsinki_gdpr:gdpr_v1", kwargs={"pk": profile.id})
        + f"?dry_run={true_value}",
    )

    assert response.status_code == 204
    assert Profile.objects.count() == 1
    assert User.objects.count() == 1


def test_delete_profile(api_client, profile, requests_mock, settings):
    auth_header = get_api_token_for_user_with_scopes(
        profile.user, [settings.GDPR_API_DELETE_SCOPE], requests_mock
    )
    api_client.credentials(HTTP_AUTHORIZATION=auth_header)
    response = api_client.delete(
        reverse("helsinki_gdpr:gdpr_v1", kwargs={"pk": profile.id})
    )

    assert response.status_code == 204
    assert Profile.objects.count() == 0
    assert User.objects.count() == 0


def test_delete_profile_dry_run_query_params_false(
    false_value, api_client, profile, requests_mock, settings
):
    auth_header = get_api_token_for_user_with_scopes(
        profile.user, [settings.GDPR_API_DELETE_SCOPE], requests_mock
    )
    api_client.credentials(HTTP_AUTHORIZATION=auth_header)
    response = api_client.delete(
        reverse("helsinki_gdpr:gdpr_v1", kwargs={"pk": profile.id})
        + f"?dry_run={false_value}",
    )

    assert response.status_code == 204
    assert Profile.objects.count() == 0
    assert User.objects.count() == 0


def test_delete_profile_dry_run_data_false(
    false_value, api_client, profile, requests_mock, settings
):
    auth_header = get_api_token_for_user_with_scopes(
        profile.user, [settings.GDPR_API_DELETE_SCOPE], requests_mock
    )
    api_client.credentials(HTTP_AUTHORIZATION=auth_header)
    response = api_client.delete(
        reverse("helsinki_gdpr:gdpr_v1", kwargs={"pk": profile.id}),
        data={"dry_run": false_value},
        format="json",
    )

    assert response.status_code == 204
    assert Profile.objects.count() == 0
    assert User.objects.count() == 0


def test_gdpr_api_requires_authentication(api_client, profile):
    response = api_client.delete(
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

    response = api_client.delete(
        reverse("helsinki_gdpr:gdpr_v1", kwargs={"pk": profile.id})
    )
    assert response.status_code == 403


@pytest.mark.parametrize("use_correct_scope", [True, False])
def test_gdpr_delete_requires_correct_scope(
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
            profile.user, [settings.GDPR_API_QUERY_SCOPE], requests_mock
        )
    api_client.credentials(HTTP_AUTHORIZATION=auth_header)

    response = api_client.delete(
        reverse("helsinki_gdpr:gdpr_v1", kwargs={"pk": profile.id})
    )

    if use_correct_scope:
        assert response.status_code == 204
    else:
        assert response.status_code == 403
        assert Profile.objects.count() == 1
        assert User.objects.count() == 1


def test_if_profile_not_found_return_404(
    api_client, user, uuid_value, requests_mock, settings
):
    auth_header = get_api_token_for_user_with_scopes(
        user, [settings.GDPR_API_DELETE_SCOPE], requests_mock
    )
    api_client.credentials(HTTP_AUTHORIZATION=auth_header)
    response = api_client.delete(
        reverse(
            "helsinki_gdpr:gdpr_v1",
            kwargs={"pk": uuid_value},
        )
    )

    assert response.status_code == 404
