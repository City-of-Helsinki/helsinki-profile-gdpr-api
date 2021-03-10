# Helsinki profile GDPR API

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
