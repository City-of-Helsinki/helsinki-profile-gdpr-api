# Changelog

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
