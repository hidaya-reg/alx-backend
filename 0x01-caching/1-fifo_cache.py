#!/usr/bin/python3
""" FIFO caching module
"""
BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """class FIFOCache
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

        self.cache_data[key] = item
        self.order.append(key)

        if len(self.order) > BaseCaching.MAX_ITEMS:
            d_key = self.order.pop(0)
            print(f"DISCARD: {d_key}")
            del self.cache_data[d_key]

    def get(self, key):
        """ Get an item by key
        """
        if key is None:
            return None
        return self.cache_data.get(key, None)
