from collections.abc import Mapping
from dataclasses import dataclass

LocalizedMessage = Mapping[str, str]
"""Human readable error messages localized to various languages: the keys specify
languages and the values are the localized messages. The language codes are not well
specified. It’s suggested that services provide any messages in Finnish (`fi`),
Swedish (`sv`) and English (`en`)."""


@dataclass
class Error:
    """Describes a single error."""

    code: str
    """A service specific error code for debugging purposes. There is no specification
    for allowed values."""
    message: LocalizedMessage


@dataclass
class ErrorResponse:
    """Response contents for providing a set of errors."""

    errors: list[Error]
