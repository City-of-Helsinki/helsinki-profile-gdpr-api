from tests.factories import ExtraDataFactory


def test_model_serialization(profile, snapshot):
    ExtraDataFactory(profile=profile)

    serialized_profile = profile.serialize()

    snapshot.assert_match(serialized_profile)
