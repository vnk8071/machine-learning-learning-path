import redis

from module.cache.base import CacheBase


class RedisCache(CacheBase):
    """Redis cache implementation."""

    def __init__(self, redis_url: str = None, key: str = "cache:", *args, **kwargs):
        """Initialize redis cache.

        Args:
            redis_url (str): Redis URL.
            key (str): Key to set value for.
            args (tuple): Positional arguments.
            kwargs (dict): Keyword arguments.

        Raises:
            ConnectionRefusedError: If redis server is not running.
        """
        super().__init__(*args, **kwargs)
        try:
            self._redis = redis.Redis.from_url(redis_url)
            self.key = key
        except Exception:
            raise ConnectionRefusedError("Redis server is not running")

    @classmethod
    def check_type(cls, type_):
        """Cache property.

        Args:
            type_ (type): Type to check.

        Returns:
            bool: True if type is allowed, False otherwise.

        Raises:
            TypeError: If type is not allowed.
        """
        try:
            return issubclass(type_, cls.allow_types)
        except TypeError:
            raise TypeError(
                f"Type must be a subclass of {cls.allow_types}, not {type_}"
            )

    @property
    def get_key(self):
        return self.key

    def get(self, key: str = None):
        """Get value from cache.

        Args:
            key (str): Key to get value for.

        Returns:
            str: Value for key.
        """
        _items = self._redis.lrange(name=self.get_key, start=0, end=-1)
        items = [m.decode("utf-8") for m in _items[::-1]]
        return items

    def add(self, value):
        """Set value in cache.

        Args:
            value (str): Value to set.
        """
        self._redis.lpush(self.get_key, value)

    def delete(self, key):
        """Delete value from cache.

        Args:
            key (str): Key to delete value for.
        """
        del self._redis[key]

    def clear(self):
        """Clear cache."""
        self._redis.clear()
