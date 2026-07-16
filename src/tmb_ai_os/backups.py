import hashlib
import json
import shutil
import sqlite3
import tarfile
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class BackupFile:
    path: str
    sha256: str
    size_bytes: int


@dataclass(frozen=True)
class BackupManifest:
    name: str
    created_at: str
    database_file: BackupFile | None
    archive_file: BackupFile | None


class BackupError(RuntimeError):
    pass


class BackupManager:
    def __init__(
        self,
        *,
        backup_dir: Path,
        database_path: Path,
        content_dir: Path,
        knowledge_dir: Path,
    ) -> None:
        self.backup_dir = backup_dir
        self.database_path = database_path
        self.content_dir = content_dir
        self.knowledge_dir = knowledge_dir

    def create(self) -> BackupManifest:
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        name = f"backup-{stamp}"
        destination = self.backup_dir / name
        destination.mkdir(parents=True, exist_ok=False)

        manifest = BackupManifest(
            name=name,
            created_at=datetime.now(UTC).isoformat(),
            database_file=self._backup_database(destination),
            archive_file=self._backup_directories(destination),
        )
        (destination / "manifest.json").write_text(
            json.dumps(
                asdict(manifest),
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        return manifest

    def list(self) -> list[BackupManifest]:
        if not self.backup_dir.exists():
            return []
        return [
            self._load_manifest(path)
            for path in sorted(
                self.backup_dir.glob("backup-*/manifest.json"),
                reverse=True,
            )
        ]

    def verify(self, name: str) -> BackupManifest:
        destination = self.backup_dir / name
        manifest_path = destination / "manifest.json"
        if not manifest_path.exists():
            raise BackupError(f"Backup not found: {name}")

        manifest = self._load_manifest(manifest_path)
        for item in (manifest.database_file, manifest.archive_file):
            if item is None:
                continue
            file_path = destination / item.path
            if not file_path.exists():
                raise BackupError(f"Missing backup file: {file_path}")
            if self._sha256(file_path) != item.sha256:
                raise BackupError(f"Checksum mismatch: {file_path}")
        return manifest

    def restore(
        self,
        name: str,
        *,
        confirm: bool,
    ) -> BackupManifest:
        if not confirm:
            raise BackupError("Restore requires explicit confirmation")

        manifest = self.verify(name)
        destination = self.backup_dir / name

        if manifest.database_file is not None:
            source = destination / manifest.database_file.path
            self.database_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, self.database_path)

        if manifest.archive_file is not None:
            archive_path = destination / manifest.archive_file.path
            with tarfile.open(archive_path, "r:gz") as archive:
                archive.extractall(Path.cwd())

        return manifest

    def _backup_database(
        self,
        destination: Path,
    ) -> BackupFile | None:
        if not self.database_path.exists():
            return None
        target = destination / "database.sqlite3"
        with sqlite3.connect(self.database_path) as source:
            with sqlite3.connect(target) as target_connection:
                source.backup(target_connection)
        return self._file_metadata(target)

    def _backup_directories(
        self,
        destination: Path,
    ) -> BackupFile | None:
        sources = [path for path in (self.content_dir, self.knowledge_dir) if path.exists()]
        if not sources:
            return None

        archive_path = destination / "content-knowledge.tar.gz"
        with tarfile.open(archive_path, "w:gz") as archive:
            for source in sources:
                archive.add(source, arcname=source.name)
        return self._file_metadata(archive_path)

    def _file_metadata(self, path: Path) -> BackupFile:
        return BackupFile(
            path=path.name,
            sha256=self._sha256(path),
            size_bytes=path.stat().st_size,
        )

    @staticmethod
    def _sha256(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    @staticmethod
    def _load_manifest(path: Path) -> BackupManifest:
        data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))

        def load_file(value: Any) -> BackupFile | None:
            if value is None:
                return None
            return BackupFile(
                path=str(value["path"]),
                sha256=str(value["sha256"]),
                size_bytes=int(value["size_bytes"]),
            )

        return BackupManifest(
            name=str(data["name"]),
            created_at=str(data["created_at"]),
            database_file=load_file(data.get("database_file")),
            archive_file=load_file(data.get("archive_file")),
        )
