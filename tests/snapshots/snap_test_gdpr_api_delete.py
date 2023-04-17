# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_deleter_function_can_provide_errors 1"] = {
    "errors": [
        {
            "code": "NO_GO",
            "message": {"en": "Can't do", "fi": "Ei pysty", "sv": "Kan inte"},
        }
    ]
}
