from __future__ import annotations

__all__ = [
    "PatchEngineError",
    "PatchValidationError",
    "TransactionError",
]


class PatchEngineError(Exception):
    """Base error raised by the patch engine."""


class PatchValidationError(PatchEngineError):
    """Raised when a patch operation fails validation."""


class TransactionError(PatchEngineError):
    """Raised when a transactional write fails."""
