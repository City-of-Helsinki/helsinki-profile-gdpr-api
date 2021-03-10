SECRET_KEY = "secret"

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "helusers.apps.HelusersConfig",
    "helusers.apps.HelusersAdminConfig",
    "helsinki_gdpr",
    "tests",
)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "tests.urls"

AUTH_USER_MODEL = "tests.User"

GDPR_API_MODEL = "tests.Profile"
GDPR_API_QUERY_SCOPE = "testprefix.gdprquery"
GDPR_API_DELETE_SCOPE = "testprefix.gdprdelete"

DEBUG = True
USE_TZ = True

OIDC_API_TOKEN_AUTH = {
    "AUDIENCE": "test_audience",
    "ISSUER": "https://test_issuer_1",
    "REQUIRE_API_SCOPE_FOR_AUTHENTICATION": False,
    "API_AUTHORIZATION_FIELD": "",
    "API_SCOPE_PREFIX": "",
}
