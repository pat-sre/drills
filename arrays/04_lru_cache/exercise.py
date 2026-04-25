# LRU Cache
#
# Implement a Least Recently Used (LRU) cache with O(1) get and put.
#
# LRUCache(capacity) initializes with a positive capacity.
# get(key)           returns the value if the key exists, else -1.
#                    marks the key as most recently used.
# put(key, value)    inserts or updates the key-value pair.
#                    marks the key as most recently used.
#                    if at capacity, evicts the least recently used key first.
#
# Example:
#   cache = LRUCache(2)
#   cache.put(1, 1)   # cache: {1: 1}
#   cache.put(2, 2)   # cache: {1: 1, 2: 2}
#   cache.get(1)      # returns 1, cache: {2: 2, 1: 1}
#   cache.put(3, 3)   # evicts key 2, cache: {1: 1, 3: 3}
#   cache.get(2)      # returns -1 (not found)
#
# Algorithm:
#   Use a doubly linked list + hashmap.
#   - The hashmap maps key -> node for O(1) lookup.
#   - The doubly linked list tracks recency: head = LRU, tail = MRU.
#   - On access or insert, move the node to the tail.
#   - On eviction, remove the head node.


class LRUCache:
    def __init__(self, capacity: int):
        pass

    def get(self, key: int) -> int:
        pass

    def put(self, key: int, value: int) -> None:
        pass


solve = LRUCache
