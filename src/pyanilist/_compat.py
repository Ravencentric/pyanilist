"""Compatibility module to for older python versions."""

from __future__ import annotations

import sys

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from backports.strenum import StrEnum


__all__ = ("StrEnum",)
