import factory
from django.contrib.auth import get_user_model

from tests.models import ExtraData, Profile

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    uuid = factory.Faker("uuid4", cast_to=None)
    first_name = "First name"
    last_name = "Last name"
    email = factory.Faker("email")

    class Meta:
        model = User


class ProfileFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    memo = "Memo"

    class Meta:
        model = Profile


class ExtraDataFactory(factory.django.DjangoModelFactory):
    profile = factory.SubFactory(ProfileFactory)
    data = "Extra"

    class Meta:
        model = ExtraData
