"""Tests for the TTL cache wrapper."""

import time
from unittest.mock import patch

from mcp_tekna.cache import cached, clear_cache


class TestCachedDecorator:
    """T007: Cache behavior tests."""

    def setup_method(self) -> None:
        clear_cache()

    def teardown_method(self) -> None:
        clear_cache()

    async def test_cache_stores_and_returns_values(self) -> None:
        call_count = 0

        @cached
        async def my_func(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2

        result1 = await my_func(5)
        result2 = await my_func(5)
        assert result1 == 10
        assert result2 == 10
        assert call_count == 1  # Second call used cache

    async def test_different_args_produce_different_keys(self) -> None:
        call_count = 0

        @cached
        async def my_func(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2

        result1 = await my_func(5)
        result2 = await my_func(10)
        assert result1 == 10
        assert result2 == 20
        assert call_count == 2  # Different args, different cache entries

    async def test_cache_can_be_cleared(self) -> None:
        call_count = 0

        @cached
        async def my_func(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2

        await my_func(5)
        clear_cache()
        await my_func(5)
        assert call_count == 2  # Cache cleared, called again

    async def test_cache_expires_after_ttl(self) -> None:
        """Test TTL expiry with a short-lived cache."""
        from cachetools import TTLCache

        short_cache = TTLCache(maxsize=10, ttl=0.1)  # 100ms TTL

        with patch("mcp_tekna.cache._cache", short_cache):
            call_count = 0

            @cached
            async def my_func(x: int) -> int:
                nonlocal call_count
                call_count += 1
                return x * 2

            await my_func(5)
            assert call_count == 1

            time.sleep(0.2)  # Wait for TTL to expire

            await my_func(5)
            assert call_count == 2  # Expired, called again
