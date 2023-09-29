from module.cache.base import CacheBase


class MemoryCache(CacheBase):
    """Memory cache implementation."""

    allow_types = [str, int, float, bool, list, dict, tuple]

    def __init__(self, *args, **kwargs):
        """Initialize memory cache.

        Args:
            args (tuple): Positional arguments.
            kwargs (dict): Keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self._cache = {}

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

    def get(self, key):
        """Get value from cache.

        Args:
            key (str): Key to get value for.

        Returns:
            str: Value for key.
        """
        return self._cache.get(key)

    def set(self, key, value):
        """Set value in cache.

        Args:
            key (str): Key to set value for.
            value (str): Value to set.
        """
        self._cache[key] = value

    def delete(self, key):
        """Delete value from cache.

        Args:
            key (str): Key to delete value for.
        """
        del self._cache[key]

    def clear(self):
        """Clear cache."""
        self._cache.clear()
