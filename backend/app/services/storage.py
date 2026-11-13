# backend/app/services/storage.py
"""Storage abstraction layer.

Currently implements a simple local filesystem storage. The interface is designed
so that a cloud storage implementation (S3, GCS, Azure) can be swapped in
without changing the rest of the application.
"""

import os
import shutil
from pathlib import Path
from abc import ABC, abstractmethod
from typing import BinaryIO

from ..core.config import settings


class BaseStorage(ABC):
    """Abstract storage interface.

    Concrete implementations must implement ``save``, ``get``, ``delete`` and
    ``exists``.
    """

    @abstractmethod
    def save(self, file_obj: BinaryIO, destination: str) -> str:
        """Save a binary file object to the given destination path.

        Args:
            file_obj: A binary file‑like object (e.g. ``UploadFile.file``).
            destination: Relative path inside the storage root (e.g. ``uploads/abc.mp3``).

        Returns:
            The absolute path where the file was stored.
        """
        raise NotImplementedError

    @abstractmethod
    def get(self, path: str) -> Path:
        """Return a ``Path`` object for the given relative ``path``.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, path: str) -> None:
        """Delete the file at ``path``.
        """
        raise NotImplementedError

    @abstractmethod
    def exists(self, path: str) -> bool:
        """Check whether a file exists at ``path``.
        """
        raise NotImplementedError


class LocalStorage(BaseStorage):
    """Local filesystem implementation.

    Files are stored under ``settings.STORAGE_ROOT`` (default ``storage``).
    The directory structure is expected to contain ``uploads``, ``processed``
    and ``generated`` sub‑folders, but the class does not enforce that – callers
    provide the full relative path they need.
    """

    def __init__(self) -> None:
        self.root = Path(settings.STORAGE_ROOT).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def _full_path(self, relative_path: str) -> Path:
        # Prevent path traversal by resolving the full path and ensuring it is
        # inside the storage root.
        candidate = (self.root / relative_path).resolve()
        if not str(candidate).startswith(str(self.root)):
            raise ValueError("Attempted path traversal outside storage root")
        return candidate

    def save(self, file_obj: BinaryIO, destination: str) -> str:
        dest_path = self._full_path(destination)
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        # Write the file in binary mode, streaming chunks to avoid loading whole
        # file into memory.
        with dest_path.open("wb") as out_file:
            shutil.copyfileobj(file_obj, out_file)
        return str(dest_path)

    def get(self, path: str) -> Path:
        return self._full_path(path)

    def delete(self, path: str) -> None:
        file_path = self._full_path(path)
        if file_path.is_file():
            file_path.unlink()

    def exists(self, path: str) -> bool:
        return self._full_path(path).exists()


# Export a singleton that can be imported throughout the project.
storage = LocalStorage()
