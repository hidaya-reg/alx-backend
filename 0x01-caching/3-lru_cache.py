#!/usr/bin/python3
""" LRU caching module
"""
BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """class LRUCache
    """

    def __init__(self):
        """Initialization
        """
        super().__init__()
        self.order = []

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return

        if key in self.cache_data.keys():
            self.order.remove(key)
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            lru_key = self.order.pop(0)
            print(f"DISCARD: {lru_key}")
            del self.cache_data[lru_key]

        self.cache_data[key] = item
        self.order.append(key)

    def get(self, key):
        """ Get an item by key
        """
        if key is None:
            return None
        self.order.remove(key)
        self.order.append(key)
        return self.cache_data[key]
