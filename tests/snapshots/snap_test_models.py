# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_model_serialization 1"] = {
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
        {
            "children": [
                {"children": [{"key": "DATA", "value": "Extra"}], "key": "EXTRADATA"}
            ],
            "key": "EXTRA_DATA",
        },
    ],
    "key": "PROFILE",
}
