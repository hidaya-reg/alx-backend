#!/usr/bin/python3
""" LFU caching module """
from collections import defaultdict, OrderedDict
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """LFUCache class with LFU caching removal mechanism."""

    def __init__(self):
        """Initialize LFUCache."""
        super().__init__()
        self.cache_data = OrderedDict()
        self.freq = defaultdict(int)
        self.lfu_keys = OrderedDict()

    def put(self, key, item):
        """Add an item to the cache with LFU eviction if necessary."""
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self._update_frequency(key)
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                self._evict_lfu_item()
            self.cache_data[key] = item
            self.freq[key] = 1
            self.lfu_keys[key] = None

    def get(self, key):
        """Retrieve an item by key."""
        if key is None or key not in self.cache_data:
            return None
        # Update frequency for accessed item
        self._update_frequency(key)
        return self.cache_data[key]

    def _update_frequency(self, key):
        """Increment the frequency of a key."""
        freq = self.freq[key]
        del self.lfu_keys[key]
        self.freq[key] += 1
        self.lfu_keys[key] = None  # Move to the most recent position

    def _evict_lfu_item(self):
        """Evict the least frequently used (LFU) item, using LRU if needed."""
        lfu_key, _ = next(iter(self.lfu_keys.items()))
        del self.cache_data[lfu_key]
        del self.freq[lfu_key]
        del self.lfu_keys[lfu_key]
        print("DISCARD:", lfu_key)
