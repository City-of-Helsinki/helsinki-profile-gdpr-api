# Changelog

## [1.0.0](https://github.com/City-of-Helsinki/helsinki-profile-gdpr-api/compare/v0.2.0...v1.0.0) (2025-04-11)


### ⚠ BREAKING CHANGES

* delete method must be of type Optional[ErrorList]

### Features

* Enforce delete result for GDPR delete ([3d4ea53](https://github.com/City-of-Helsinki/helsinki-profile-gdpr-api/commit/3d4ea5365a4fe3cad52e3787e2714d5d4c90248f))
* Required at least Django 4.2 and Python 3.9 ([03cf602](https://github.com/City-of-Helsinki/helsinki-profile-gdpr-api/commit/03cf6026209f04dfb75a06d074ccacc77815cc3e))


### Documentation

* **readme:** Add ruff and commitlint ([d8a8a66](https://github.com/City-of-Helsinki/helsinki-profile-gdpr-api/commit/d8a8a66ad1d488e87f5ad2c132bfddb4e2c87b6d))

## 0.2.0 - 2023-04-18

### Added

- `GDPR_API_URL_PATTERN` setting for configuring the GDPR API URL pattern.
- `GDPR_API_MODEL_LOOKUP` setting for configuring how the GDPR model instance is found.
- `GDPR_API_USER_PROVIDER` setting for configuring how to obtain a `User` instance from the GDPR model instance.
- `GDPR_API_DELETER` setting for configuring how data deletion is performed.

### Changed

- Respond with a `204 No Content` status code when no data is found for the requested profile.

### Removed

- Support for Python 3.6
- `helsinki_gdpr.views.DeletionNotAllowed` exception class. Raising that exception produced responses with
  contents that are against the GDPR API specification. A user specified function configured with the
  `GDPR_API_DELETER` setting should be used instead.

## 0.1.0 - 2021-03-15

Release the initial version of the module.
