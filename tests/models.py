import uuid

from django.conf import settings
from django.db import DatabaseError, models
from helusers.models import AbstractUser

from helsinki_gdpr.models import SerializableMixin


class User(AbstractUser, SerializableMixin):
    serialize_fields = (
        {"name": "first_name"},
        {"name": "last_name"},
    )


class Profile(SerializableMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    memo = models.CharField(max_length=128, blank=True)

    serialize_fields = (
        {"name": "memo"},
        {"name": "user"},
        {"name": "user", "accessor": lambda x: f"{x.first_name} {x.last_name}"},
        {"name": "extra_data"},
    )

    def delete(self, **kwargs):
        if self.memo == "nodelete":
            raise DatabaseError()
        return super().delete(**kwargs)


class ExtraData(SerializableMixin):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="extra_data",
    )
    data = models.CharField(max_length=255)

    serialize_fields = ({"name": "data"},)
