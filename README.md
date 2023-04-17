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

If changing the field lookup that way doesn't solve the model instance searching, it's also possible to
set the `GDPR_API_MODEL_LOOKUP` setting to an import path to a function, for example
`myapp.gdpr.get_model_instance`. The function gets called whenever the GDPR API is accessed and the model
instance is needed. The function gets two arguments, the model class specified by the `GDPR_API_MODEL`
setting and the id from the GDPR API request's path. The function must return an instance of the model
specified by the `GDPR_API_MODEL` setting, if an instance is found. If no instance is found, then the
function must either return `None` or raise a `DoesNotExist` exception of the model.

### Obtaining a User model instance

It's required that a `User` model instance can be obtained from the GDPR API model instance specified by
the `GDPR_API_MODEL` setting. By default the GDPR API model instance's `user` attribute is tried. If that
doesn't work, it's possible to configure a function that will provide the `User` instance. This is
achieved by setting the import path of the function to the `GDPR_API_USER_PROVIDER` setting, for example
`myapp.gdpr.get_user`. The function gets the GDPR API model instance as an argument.

### Controlling how data deletion is performed

By default the GDPR delete operation deletes the `GDPR_API_MODEL` instance and the related `User`
instance. If that procedure isn't sufficient for the project, it's possible to override the data deletion
operation. This is achieved by setting the `GDPR_API_DELETER` setting to an import path to a function, for
example `myapp.gdpr.delete_data`. The function gets two arguments, the `GDPR_API_MODEL` instance and a
boolean value indicating if this is a dry run or not.

The function gets called within a database transaction, which gets automatically rolled back if it's a dry
run operation. Thus the function is free to do database modifications even in the dry run case. All
changes get rolled back afterwards. If it's not a dry run case, then the transaction is committed and all
changes to the database are persisted.

If the data deletion isn't allowed, the function has two ways to indicate this:

- Return a `helsinki_gdpr.types.ErrorResponse` instance. This allows also communicating the reasons
  why the deletion isn't allowed.
- Raise a `django.db.DatabaseError` exception.

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
