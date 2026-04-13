"""
helpers.py
==========
Shared utility functions used across the CollabLearn system.
"""

from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone
from pathlib import Path


def utc_now_iso() -> str:
    """Return the current UTC time as an ISO 8601 string.

    Returns:
        ISO 8601 formatted UTC timestamp string.
    """
    return datetime.now(timezone.utc).isoformat()


def generate_session_id(learner_id: str, timestamp: str) -> str:
    """Generate a deterministic session ID from learner ID and timestamp.

    Args:
        learner_id: The learner's unique identifier.
        timestamp: ISO 8601 timestamp string.

    Returns:
        A short hexadecimal session ID string (12 characters).
    """
    raw = f"{learner_id}:{timestamp}"
    return hashlib.sha256(raw.encode()).hexdigest()[:12]


def sanitize_filename(name: str) -> str:
    """Convert a string to a safe filename.

    Replaces spaces with hyphens, removes special characters,
    and converts to lowercase.

    Args:
        name: The raw string to sanitize.

    Returns:
        A safe, lowercase filename string.

    Examples:
        >>> sanitize_filename("Hello World! (2026)")
        'hello-world-2026'
    """
    name = name.lower()
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s_]+", "-", name)
    name = name.strip("-")
    return name


def ensure_dir(path: str | Path) -> Path:
    """Ensure a directory exists, creating it and all parents if necessary.

    Args:
        path: The directory path to create.

    Returns:
        The resolved Path object.
    """
    p = Path(path).resolve()
    p.mkdir(parents=True, exist_ok=True)
    return p


def truncate_text(text: str, max_chars: int = 500, suffix: str = "...") -> str:
    """Truncate text to a maximum character length.

    Args:
        text: The text to truncate.
        max_chars: Maximum number of characters before truncation.
        suffix: String appended to truncated text.

    Returns:
        The original text if within limit, or truncated text with suffix.
    """
    if len(text) <= max_chars:
        return text
    return text[: max_chars - len(suffix)] + suffix


def count_words(text: str) -> int:
    """Count the number of words in a text string.

    Args:
        text: The text to count words in.

    Returns:
        Word count as an integer.
    """
    return len(text.split())


def format_duration(start_iso: str, end_iso: str) -> str:
    """Format the duration between two ISO 8601 timestamps as a human-readable string.

    Args:
        start_iso: ISO 8601 start timestamp.
        end_iso: ISO 8601 end timestamp.

    Returns:
        Duration string, e.g., '5m 23s' or '1h 12m'.
    """
    start = datetime.fromisoformat(start_iso)
    end = datetime.fromisoformat(end_iso)
    delta = end - start
    total_seconds = int(delta.total_seconds())

    if total_seconds < 0:
        return "0s"

    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts = []
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if seconds or not parts:
        parts.append(f"{seconds}s")
    return " ".join(parts)
