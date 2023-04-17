from django.conf import settings
from django.urls import path

from helsinki_gdpr.views import GDPRAPIView

app_name = "helsinki_gdpr"
urlpatterns = [
    path(
        getattr(settings, "GDPR_API_URL_PATTERN", "v1/profiles/<uuid:pk>"),
        GDPRAPIView.as_view(),
        name="gdpr_v1",
    ),
]
