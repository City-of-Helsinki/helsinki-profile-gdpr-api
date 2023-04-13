# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_get_profile_information_from_gdpr_api 1"] = {
    "children": [
        {"key": "MEMO", "value": "Memo"},
        {
            "children": [
                {"key": "FIRST_NAME", "value": "First name"},
                {"key": "LAST_NAME", "value": "Last name"},
            ],
            "key": "USER",
        },
        {"key": "USER", "value": "First name Last name"},
        {"children": [], "key": "EXTRA_DATA"},
    ],
    "key": "PROFILE",
}

snapshots["test_model_lookup_can_be_configured_to_a_field 1"] = {
    "children": [
        {"key": "MEMO", "value": "Memo"},
        {
            "children": [
                {"key": "FIRST_NAME", "value": "First name"},
                {"key": "LAST_NAME", "value": "Last name"},
            ],
            "key": "USER",
        },
        {"key": "USER", "value": "First name Last name"},
        {"children": [], "key": "EXTRA_DATA"},
    ],
    "key": "PROFILE",
}

snapshots[
    "test_model_lookup_can_be_configured_to_a_function[model_lookup_that_returns_none-True] 1"
] = {
    "children": [
        {"key": "MEMO", "value": "Memo"},
        {
            "children": [
                {"key": "FIRST_NAME", "value": "First name"},
                {"key": "LAST_NAME", "value": "Last name"},
            ],
            "key": "USER",
        },
        {"key": "USER", "value": "First name Last name"},
        {"children": [], "key": "EXTRA_DATA"},
    ],
    "key": "PROFILE",
}

snapshots[
    "test_model_lookup_can_be_configured_to_a_function[model_lookup_that_throws_exception-True] 1"
] = {
    "children": [
        {"key": "MEMO", "value": "Memo"},
        {
            "children": [
                {"key": "FIRST_NAME", "value": "First name"},
                {"key": "LAST_NAME", "value": "Last name"},
            ],
            "key": "USER",
        },
        {"key": "USER", "value": "First name Last name"},
        {"children": [], "key": "EXTRA_DATA"},
    ],
    "key": "PROFILE",
}

snapshots["test_user_provider_function_can_be_configured 1"] = {
    "children": [{"key": "DATA", "value": "Extra"}],
    "key": "EXTRADATA",
}
