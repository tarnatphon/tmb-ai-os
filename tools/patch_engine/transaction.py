from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from . import TransactionError
from .writer import atomic_write_text


@dataclass(frozen=True, slots=True)
class FileReplacement:
    """A complete replacement for one text file."""

    path: Path
    content: str


class PatchTransaction:
    """Apply text replacements and roll back if any write fails."""

    def __init__(self) -> None:
        self._backups: dict[Path, str | None] = {}
        self._committed = False

    def apply(self, replacements: tuple[FileReplacement, ...], *, commit: bool = True) -> None:
        """Apply all replacements transactionally."""

        try:
            for replacement in replacements:
                self._backup(replacement.path)
                atomic_write_text(replacement.path, replacement.content)
        except OSError as exc:
            self.rollback()
            raise TransactionError(f"failed to apply patch transaction: {exc}") from exc

        if commit:
            self.commit()

    def commit(self) -> None:
        """Mark the transaction as successful."""

        self._committed = True

    def rollback(self) -> None:
        """Restore files captured before the transaction."""

        if self._committed:
            return

        for path, previous_content in reversed(tuple(self._backups.items())):
            if previous_content is None:
                path.unlink(missing_ok=True)
            else:
                atomic_write_text(path, previous_content)

    def _backup(self, path: Path) -> None:
        if path in self._backups:
            return

        if path.exists():
            self._backups[path] = path.read_text(encoding="utf-8")
            return

        self._backups[path] = None
