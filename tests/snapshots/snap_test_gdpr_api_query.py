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
