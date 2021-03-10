from django.urls import include, path

urlpatterns = [path("gdpr-api/", include("helsinki_gdpr.urls"))]
