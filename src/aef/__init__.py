"""Apex Elite Framework."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("apex-elite-framework")
except PackageNotFoundError:  # pragma: no cover - execução direta do código-fonte
    __version__ = "1.0.1rc1"

__all__ = ["__version__"]

