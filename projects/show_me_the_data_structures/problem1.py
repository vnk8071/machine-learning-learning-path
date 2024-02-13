"""
Course: Data Structures & Algorithms
Core: Data Structures
Problem: 1
Code by: KhoiVN
Date: 04/01/2024
"""


class LRUCache(object):

    def __init__(self, capacity):
        # Initialize class variables
        if not isinstance(capacity, int) or capacity < 0:
            self.capacity = 0
        else:
            self.capacity = capacity
        self.lru_cache = {}

    def __repr__(self):
        return f"LRUCache({self.lru_cache})"

    def get(self, key):
        return self.lru_cache.get(key, -1)

    def set(self, key, value):
        self.lru_cache[key] = value
        if len(self.lru_cache) > self.capacity and self.capacity != 0:
            self.lru_cache.pop(list(self.lru_cache.keys())[0])


our_cache = LRUCache(5)

our_cache.set(1, 1)
our_cache.set(2, 2)
our_cache.set(3, 3)
our_cache.set(4, 4)

print(our_cache)

# Test Case 1
print("Test Case 1", our_cache)
assert our_cache.get(1) == 1
assert our_cache.get(2) == 2
assert our_cache.get(9) == -1

our_cache.set(5, 5)
our_cache.set(6, 6)

# Test Case 2
print("Test Case 2", our_cache)
assert our_cache.get(4) == 4

# Test Case 3
print("Test Case 3", our_cache)
assert our_cache.get(1) == -1
assert our_cache.get(3) == 3
assert our_cache.get(100) == -1

# Edge Test Case 1
our_cache = LRUCache(0)
print("Edge Test Case 1.1", our_cache)
assert our_cache.get(1) == -1

our_cache = LRUCache(100)
print("Edge Test Case 1.2", our_cache)
assert our_cache.get(1) == -1

# Edge Case 2
our_cache = LRUCache(None)
print("Edge Test Case 2", our_cache)
assert our_cache.get(1) == -1

print("All test cases pass")
