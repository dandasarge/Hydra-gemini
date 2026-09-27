"""Enumerations used across Hydra."""

from __future__ import annotations

from enum import Enum


class GeminiModel(str, Enum):
    """Supported Gemini models on the free tier."""

    GEMINI_37_FLASH = "gemini-3.7-flash"
    GEMINI_36_FLASH = "gemini-3.6-flash"
    GEMINI_35_FLASH = "gemini-3.5-flash"
    GEMINI_3_FLASH = "gemini-3-flash-preview"
    GEMINI_35_FLASH_LITE = "gemini-3.5-flash-lite"
    GEMINI_31_FLASH_LITE = "gemini-3.1-flash-lite"
    GEMINI_25_FLASH_LITE = "gemini-2.5-flash-lite"


class KeyStatus(str, Enum):
    """Health status of an API key."""

    OK = "ok"
    HIGH_USAGE = "high_usage"
    MAX = "max"
    DISABLED = "disabled"
    UNKNOWN = "unknown"

