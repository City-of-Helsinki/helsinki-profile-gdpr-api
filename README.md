# Helsinki profile GDPR API

[![CI workflow](https://github.com/City-of-Helsinki/helsinki-profile-gdpr-api/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/City-of-Helsinki/helsinki-profile-gdpr-api/actions/workflows/ci.yml?query=branch:main)
[![codecov](https://codecov.io/gh/City-of-Helsinki/helsinki-profile-gdpr-api/branch/main/graph/badge.svg)](https://codecov.io/gh/City-of-Helsinki/helsinki-profile-gdpr-api)
[![PyPI](https://badgen.net/pypi/v/helsinki-profile-gdpr-api)](https://pypi.org/project/helsinki-profile-gdpr-api/)

Django app for implementing Helsinki profile GDPR API.

This library will allow a service using Helsinki profile to implement the GDPR
functionality required by [open-city-profile](https://github.com/City-of-Helsinki/open-city-profile)
backend.

## Installation

1. `pip install helsinki-profile-gdpr-api`

## Usage

1. Authentication needs to be configured for the required `django-heluser`

2. Model which is to be used for GDPR operations should inherit `SerializableMixin` and
   include the required `serialize_fields` property.

3. Define the following settings in your Django configuration.

    | Setting | Example | Description |
    |---|---|---|
    | GDPR_API_MODEL | "youths.YouthProfile" | GDPR profile model in the form `app_label.model_name`. model_name is case-insensitive. |
    | GDPR_API_QUERY_SCOPE | "jassariapi.gdprquery" | API scope required for the query operation. |
    | GDPR_API_DELETE_SCOPE | "jassariapi.gdprdelete" | API scope required for the delete operation. |

4. Add the GDPR API urls into your url config:

    ```python
    urlpatterns = [
        ...
        path("gdpr-api/", include("helsinki_gdpr.urls")),
    ]
    ```

## Configurability

The configuration above is the minimum needed. With those the app uses the default behaviour.
The app can also be configured in various ways if the default behaviour is not appropriate.

### Searching the model instance

By default the `GDPR_API_MODEL` is searched with its primary key, something like this:

```python
from django.apps import apps
from django.conf import settings

model = apps.get_model(settings.GDPR_API_MODEL)
# The `id` is extracted from the request's URL
obj = model.objects.get(pk=id)
```

If `pk` is not the correct field lookup to use, set the setting `GDPR_API_MODEL_LOOKUP` to the correct
value, for example `user__uuid`.

## Development

It's good to use a Python virtual environment:

    $> python -m venv venv
    $> source ./venv/bin/activate

Install development dependencies:

    $> pip install -r requirements-dev.txt

Run tests:

    $> pytest

## Code format

This project uses
[`black`](https://github.com/ambv/black),
[`flake8`](https://gitlab.com/pycqa/flake8) and
[`isort`](https://github.com/timothycrosley/isort)
for code formatting and quality checking. Project follows the basic black config, without any modifications.

Basic `black` commands:

* To let `black` do its magic: `black .`
* To see which files `black` would change: `black --check .`

[`pre-commit`](https://pre-commit.com/) can be used to install and run all the formatting tools as git hooks
automatically before a commit.
