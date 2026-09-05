"""Compatibility wrapper for legacy repository imports."""

from .storage.sqlite_repository import SQLiteRepository

__all__ = ["SQLiteRepository"]
