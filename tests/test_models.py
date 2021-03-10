from tests.factories import ExtraDataFactory


def test_model_serialization(profile, snapshot):
    profile.user.first_name = "First"
    profile.user.save()
    ExtraDataFactory(profile=profile)

    serialized_profile = profile.serialize()

    snapshot.assert_match(serialized_profile)
