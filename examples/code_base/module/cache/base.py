# Description: Base class for cache implementations.


class CacheBase(object):
    """Base class for cache implementations.

    Attributes:
        allow_types (list): Allowed types for cache.
    """

    allow_types = []

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def check_type(cls, type_):
        """Check type of cache.

        Args:
            type_ (type): Type to check.

        Returns:
            bool: True if type is allowed, False otherwise.
        """
        return type_ in cls.allow_types

    @property
    def get_key(self):
        """Get key for cache.
        """
        pass

    def get(self, key: str = None):
        raise NotImplementedError

    def set(self, key, value):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError
