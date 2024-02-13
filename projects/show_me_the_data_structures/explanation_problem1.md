# Least Recently Used (LRU) Cache

Time Complexity:

- `get(key)`: The time complexity is O(1) because it uses a dictionary (hashmap) to retrieve the value associated with a key.
- `set(key, value)`: The time complexity is O(1) for setting a new key-value pair in the dictionary. However, when the capacity of the cache is exceeded, the oldest item (first item in the dictionary) is removed, which takes O(n) time because it involves creating a list of keys and accessing the first one.

Space Complexity: The space complexity is O(n), where n is the capacity of the cache. This is because a dictionary is used to store the key-value pairs, and the size of the dictionary is at most the capacity of the cache.

However, the current implementation does not fully satisfy the requirements of an LRU Cache. In an LRU Cache, the get operation should also update the "recently used" status of the key. The set operation, when the capacity is exceeded, should remove the least recently used item, not just the oldest item. To achieve this, a combination of a doubly linked list (to keep track of the order of usage) and a dictionary (for O(1) access) is typically used. This would still maintain the O(1) time complexity for get and set operations, and O(n) space complexity.
