import pytest
from app.auth import redis as redis_utils

@pytest.mark.asyncio
async def test_get_redis(monkeypatch):
    """Test get_redis returns a redis instance (mocked)"""
    class FakeRedis:
        pass
    async def fake_from_url(url):
        return FakeRedis()
    monkeypatch.setattr(redis_utils.redis, "from_url", fake_from_url)
    # Remove cached instance if present
    if hasattr(redis_utils.get_redis, "redis"):
        delattr(redis_utils.get_redis, "redis")
    instance = await redis_utils.get_redis()
    assert isinstance(instance, FakeRedis)
    # Should return cached instance on second call
    instance2 = await redis_utils.get_redis()
    assert instance is instance2

@pytest.mark.asyncio
async def test_add_to_blacklist(monkeypatch):
    """Test add_to_blacklist calls redis.set with correct args"""
    called = {}
    class FakeRedis:
        async def set(self, key, value, ex=None):
            called["key"] = key
            called["value"] = value
            called["ex"] = ex
    async def fake_from_url(url):
        return FakeRedis()
    monkeypatch.setattr(redis_utils.redis, "from_url", fake_from_url)
    if hasattr(redis_utils.get_redis, "redis"):
        delattr(redis_utils.get_redis, "redis")
    await redis_utils.add_to_blacklist("jti123", 1234)
    assert called["key"] == "blacklist:jti123"
    assert called["value"] == "1"
    assert called["ex"] == 1234

@pytest.mark.asyncio
async def test_is_blacklisted(monkeypatch):
    """Test is_blacklisted returns True/False as expected"""
    class FakeRedis:
        def __init__(self, exists_result):
            self._exists_result = exists_result
        async def exists(self, key):
            return self._exists_result
    async def fake_from_url(url):
        return FakeRedis(True)
    monkeypatch.setattr(redis_utils.redis, "from_url", fake_from_url)
    if hasattr(redis_utils.get_redis, "redis"):
        delattr(redis_utils.get_redis, "redis")
    result = await redis_utils.is_blacklisted("jti123")
    assert result is True

    async def fake_from_url_false(url):
        return FakeRedis(False)
    monkeypatch.setattr(redis_utils.redis, "from_url", fake_from_url_false)
    if hasattr(redis_utils.get_redis, "redis"):
        delattr(redis_utils.get_redis, "redis")
    result = await redis_utils.is_blacklisted("jti123")
    assert result is False
