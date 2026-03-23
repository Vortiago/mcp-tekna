"""TTL cache wrapper for Tekna API responses."""

import hashlib
import json
import os
from functools import wraps
from typing import Any

from cachetools import TTLCache

_DEFAULT_TTL = 15 * 60  # 15 minutes
_MAX_SIZE = 256

_ttl = int(os.getenv("TEKNA_CACHE_TTL", str(_DEFAULT_TTL)))
_cache: TTLCache = TTLCache(maxsize=_MAX_SIZE, ttl=_ttl)


def _make_key(func_name: str, args: tuple, kwargs: dict) -> str:
    """Create a deterministic cache key from function name and arguments."""
    raw = json.dumps({"fn": func_name, "args": args, "kw": kwargs}, sort_keys=True)
    return hashlib.md5(raw.encode()).hexdigest()


def cached(func: Any) -> Any:
    """Decorator that caches async function results with TTL."""

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        key = _make_key(func.__name__, args, kwargs)
        if key in _cache:
            return _cache[key]
        result = await func(*args, **kwargs)
        _cache[key] = result
        return result

    return wrapper


def clear_cache() -> None:
    """Clear all cached entries."""
    _cache.clear()
