# Changelog

## [1.0.3](https://github.com/City-of-Helsinki/helsinki-profile-gdpr-api/compare/v1.0.2...v1.0.3) (2026-03-17)


### Dependencies

* Bump authlib from 1.6.7 to 1.6.9 ([4cb2ff9](https://github.com/City-of-Helsinki/helsinki-profile-gdpr-api/commit/4cb2ff9751a5adbf75688b11862046f1632f6151))
* Bump urllib3 from 2.3.0 to 2.6.3 ([ad15f52](https://github.com/City-of-Helsinki/helsinki-profile-gdpr-api/commit/ad15f52e6b4fb06430d72ce9e2a8d3087fb1fc87))

## [1.0.2](https://github.com/City-of-Helsinki/helsinki-profile-gdpr-api/compare/v1.0.1...v1.0.2) (2026-03-11)


### Dependencies

* Bump authlib from 1.5.1 to 1.6.6 ([b79b57e](https://github.com/City-of-Helsinki/helsinki-profile-gdpr-api/commit/b79b57ef384fe657270ebc63af90aa050c7563a9))
* Bump authlib from 1.6.6 to 1.6.7 ([f8bbf7a](https://github.com/City-of-Helsinki/helsinki-profile-gdpr-api/commit/f8bbf7aa29dbd0a92af41dfd7a7c44dac9c34bad))
* Bump django from 4.2.20 to 4.2.28 ([b62793f](https://github.com/City-of-Helsinki/helsinki-profile-gdpr-api/commit/b62793f32fc29f92e14e7ca23aa179c3d1c69be2))
* Bump django from 4.2.28 to 4.2.29 ([d6f607a](https://github.com/City-of-Helsinki/helsinki-profile-gdpr-api/commit/d6f607a2b8b8b34937245d378bd7fbf7a210fcb6))
* Bump requests from 2.32.3 to 2.32.4 ([27eff4d](https://github.com/City-of-Helsinki/helsinki-profile-gdpr-api/commit/27eff4d233a507b4f7c0abe22fc51e932eb7f4de))
* Bump sqlparse from 0.5.3 to 0.5.4 ([29aaaae](https://github.com/City-of-Helsinki/helsinki-profile-gdpr-api/commit/29aaaaec90bee0299ca9dfaed737cc061942c6c8))
* Bump wheel from 0.45.1 to 0.46.2 ([e08c9d9](https://github.com/City-of-Helsinki/helsinki-profile-gdpr-api/commit/e08c9d9d7aa74821e5ba1b1e8b56409aa8643c42))

## [1.0.1](https://github.com/City-of-Helsinki/helsinki-profile-gdpr-api/compare/v1.0.0...v1.0.1) (2025-11-05)


### Dependencies

* Add support for Python 3.14, drop support for Python 3.9 ([a4baef8](https://github.com/City-of-Helsinki/helsinki-profile-gdpr-api/commit/a4baef85942a5cd4e574e23540cd755a7e20715b))

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
