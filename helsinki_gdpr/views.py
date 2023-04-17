import dataclasses

from django.apps import apps
from django.conf import settings
from django.db import DatabaseError, transaction
from django.utils.module_loading import import_string
from helusers.oidc import ApiTokenAuthentication
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from helsinki_gdpr.models import SerializableMixin
from helsinki_gdpr.types import ErrorResponse


class DryRunException(Exception):
    """Indicate that request is being done as a dry run."""


class DryRunSerializer(serializers.Serializer):
    dry_run = serializers.BooleanField(required=False, default=False)


def _try_setting_import(setting_name):
    setting_value = getattr(settings, setting_name, None)
    if setting_value:
        try:
            return import_string(setting_value)
        except ImportError:
            pass

    return setting_value


def _user_from_obj(obj):
    user_provider = _try_setting_import("GDPR_API_USER_PROVIDER")
    if callable(user_provider):
        return user_provider(obj)

    return getattr(obj, "user", None)


def _default_deleter(obj, dry_run):
    user = _user_from_obj(obj)
    obj.delete()
    if user:
        user.delete()


class GDPRScopesPermission(IsAuthenticated):
    def has_permission(self, request, view):
        authenticated = super().has_permission(request, view)
        if authenticated:
            if request.method == "GET":
                return request.auth.has_api_scopes(settings.GDPR_API_QUERY_SCOPE)
            elif request.method == "DELETE":
                return request.auth.has_api_scopes(settings.GDPR_API_DELETE_SCOPE)
        return False

    def has_object_permission(self, request, view, obj):
        return request.user == _user_from_obj(obj)


class GDPRAPIView(APIView):
    """Fetch or delete all information related to the profile."""

    renderer_classes = [JSONRenderer]
    authentication_classes = [ApiTokenAuthentication]
    permission_classes = [GDPRScopesPermission]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = apps.get_model(settings.GDPR_API_MODEL)

        custom_model_lookup = _try_setting_import("GDPR_API_MODEL_LOOKUP")
        if callable(custom_model_lookup):
            self.model_lookup = custom_model_lookup
        else:
            lookup_key = custom_model_lookup or "pk"

            def model_lookup(model, instance_id):
                field_lookups = {lookup_key: instance_id}
                return model.objects.get(**field_lookups)

            self.model_lookup = model_lookup

    def get_object(self) -> SerializableMixin:
        obj = self.model_lookup(self.model, self.kwargs["pk"])
        if obj is None:
            raise self.model.DoesNotExist()
        self.check_object_permissions(self.request, obj)
        return obj

    def is_dry_run(self):
        """Check if parameters provided to the view indicate it's being used for dry_run."""
        data = DryRunSerializer(data=self.request.data)
        query = DryRunSerializer(data=self.request.query_params)
        data.is_valid()
        query.is_valid()

        return data.validated_data["dry_run"] or query.validated_data["dry_run"]

    def get(self, request, *args, **kwargs):
        """Retrieve all profile data related to the given id."""
        try:
            return Response(self.get_object().serialize(), status=status.HTTP_200_OK)
        except self.model.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        """Delete all data related to the given profile.

        Deletes all data related to the given profile id, or just checks if the data can be deleted,
        depending on the `dry_run` parameter. Raises DeletionNotAllowed if the item

        Dry run delete is expected to always give the same end result as the proper delete i.e. if
        dry run indicated deleting is OK, the proper delete should be OK too.
        """

        class DeletionDeniedException(Exception):
            """Indicate that data deletion is denied."""

        deleter = _try_setting_import("GDPR_API_DELETER")

        if not callable(deleter):
            deleter = _default_deleter

        dry_run = self.is_dry_run()

        try:
            with transaction.atomic():
                obj = self.get_object()
                delete_result = deleter(obj, dry_run)
                if isinstance(delete_result, ErrorResponse):
                    raise DeletionDeniedException()
                if dry_run:
                    raise DryRunException()
        except self.model.DoesNotExist:
            pass
        except DryRunException:
            # Deletion is possible. Due to dry run, transaction is rolled back.
            pass
        except DeletionDeniedException:
            return Response(
                data=dataclasses.asdict(delete_result), status=status.HTTP_403_FORBIDDEN
            )
        except DatabaseError:
            return Response(status=status.HTTP_403_FORBIDDEN)

        return Response(status=status.HTTP_204_NO_CONTENT)
