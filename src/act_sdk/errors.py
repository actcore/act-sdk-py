"""ACT error types."""


class ActError(Exception):
    """ACT tool error with a kind and message."""

    def __init__(self, kind: str, message: str) -> None:
        super().__init__(message)
        self.kind = kind
        self.message = message

    @classmethod
    def not_found(cls, message: str) -> "ActError":
        return cls("std:not-found", message)

    @classmethod
    def invalid_args(cls, message: str) -> "ActError":
        return cls("std:invalid-args", message)

    @classmethod
    def internal(cls, message: str) -> "ActError":
        return cls("std:internal", message)

    @classmethod
    def timeout(cls, message: str) -> "ActError":
        return cls("std:timeout", message)

    @classmethod
    def capability_denied(cls, message: str) -> "ActError":
        return cls("std:capability-denied", message)
