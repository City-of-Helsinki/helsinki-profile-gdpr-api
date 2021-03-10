import uuid

from django.conf import settings
from django.db import models
from helusers.models import AbstractUser

from helsinki_gdpr.models import SerializableMixin


class User(AbstractUser):
    pass


class Profile(SerializableMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    memo = models.CharField(max_length=128, blank=True)

    serialize_fields = (
        {"name": "memo"},
        {"name": "user", "accessor": lambda x: x.first_name},
        {"name": "extra_data"},
    )


class ExtraData(SerializableMixin):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="extra_data",
    )
    data = models.CharField(max_length=255)

    serialize_fields = ({"name": "data"},)
