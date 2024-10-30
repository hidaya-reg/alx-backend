# 0x01. Caching
## Resources
- [Cache replacement policies - FIFO](https://en.wikipedia.org/wiki/Cache_replacement_policies#First_In_First_Out_%28FIFO%29)
- [Cache replacement policies - LIFO](https://en.wikipedia.org/wiki/Cache_replacement_policies#Last_In_First_Out_%28LIFO%29)
- [Cache replacement policies - LRU](https://en.wikipedia.org/wiki/Cache_replacement_policies#Least_Recently_Used_%28LRU%29)
- [Cache replacement policies - MRU](https://en.wikipedia.org/wiki/Cache_replacement_policies#Most_Recently_Used_%28MRU%29)
- [Cache replacement policies - LFU](https://en.wikipedia.org/wiki/Cache_replacement_policies#Least-Frequently_Used_%28LFU%29)

## Learning Objectives
<details>
<summary>What a caching system is</summary>

### Caching system
A caching system is a mechanism that stores copies of data in a temporary storage layer (the "cache") so that future requests for that data can be served faster. Caches help improve performance by reducing the need to access the primary data source, which is often slower or more resource-intensive, such as a database or external API.

#### Key Concepts of Caching
**1. Temporary Storage:** Data is stored temporarily, meaning it may be discarded after a certain time or when space runs out.
**2. Speed:** Caches are designed to provide rapid access to frequently requested data.
**3. Efficiency:** By storing results of expensive operations (like database queries), caches reduce processing time and resource usage.
#### How Caching Works
When a request for data is made:
**- First**, the system checks the cache to see if the data is already there (a cache "hit").
**- If not**, it retrieves the data from the original source (a cache "miss") and adds it to the cache for future use.
#### Caching Strategies
Caching systems often use strategies to decide which data to keep or discard:
- **FIFO (First In, First Out):** Evicts the oldest added item in the cache when space is needed.
- **LIFO (Last In, First Out):** Evicts the most recently added item in the cache.
- **LRU (Least Recently Used):** Removes the item that hasn’t been accessed for the longest time.
- **MRU (Most Recently Used):** Removes the item that was most recently accessed.
- **LFU (Least Frequently Used):** Discards the least frequently accessed item in the cache.
#### Benefits of Caching
**- Performance Improvement:** Reduces latency by serving frequently accessed data more quickly.
**- Reduced Load on Resources:** Decreases the number of requests to the primary data source.
**- Cost Efficiency:** Saves processing power and bandwidth, especially in large systems.

Caches are widely used in applications like web servers, databases, and content delivery networks (CDNs) to improve response times and overall system performance.
</details>
<details>
<summary>Implement Caching in python</summary>

### Caching implementation
#### 1. Using a Dictionary (Simple In-Memory Cache)
This is a basic way to store and retrieve data with key-value pairs, but you need to manage cache expiration and size manually.
```python
class SimpleCache:
    def __init__(self):
        self.cache = {}

    def put(self, key, value):
        self.cache[key] = value

    def get(self, key):
        return self.cache.get(key)

# Usage
cache = SimpleCache()
cache.put("user:1", {"name": "Alice"})
print(cache.get("user:1"))  # Output: {'name': 'Alice'}
```
#### 2. Using ``functools.lru_cache`` (Built-in LRU Cache Decorator)
The ``lru_cache`` decorator from ``functools`` is an easy way to add caching to functions, with automatic management of cache size based on Least Recently Used (LRU) strategy.
```python
from functools import lru_cache

@lru_cache(maxsize=4)
def expensive_operation(x):
    print("Computing...")
    return x * x

# Usage
print(expensive_operation(2))  # Computing... 4
print(expensive_operation(2))  # 4 (cached result, no computation)
```
#### 3. Using ``cachetools`` Library (Customizable Caching Strategies)
The ``cachetools`` library provides more customizable caching strategies, including LRU, LFU, and TTL (time-to-live) caches.

First, install ``cachetools``: `pip install cachetools`

Then, you can use it as follows:
```python
from cachetools import LRUCache

cache = LRUCache(maxsize=4)
cache['a'] = 1
cache['b'] = 2
cache['c'] = 3
cache['d'] = 4
print(cache)  # {'a': 1, 'b': 2, 'c': 3, 'd': 4}

cache['e'] = 5  # Adds 'e' and evicts the least recently used item ('a')
print(cache)  # {'b': 2, 'c': 3, 'd': 4, 'e': 5}
```
#### 4. Using Redis (Persistent, Distributed Cache)
Redis is a popular in-memory data store, which can be used for caching in distributed systems. You’ll need the ``redis`` library and a running Redis server.
```bash
pip install redis
```
**Example of using Redis as a cache:**
```python
import redis

cache = redis.Redis(host='localhost', port=6379, db=0)

def put(key, value):
    cache.set(key, value)

def get(key):
    return cache.get(key)

# Usage
put("username", "Alice")
print(get("username"))  # b'Alice'
```
#### Choosing the Right Caching Strategy
- Use simple dictionaries for small, temporary caches within a program.
- Use ``lru_cache`` for caching function outputs with minimal setup.
- Use ``cachetools`` if you need specific caching policies like LFU.
- Use **Redis** for distributed, persistent caching across multiple applications.
</details>
<details>
<summary>What FIFO means</summary>

### FIFO (First In, First Out)
**FIFO (First In, First Out)** caching is a caching strategy where the oldest item added to the cache is removed first when the cache reaches its maximum size. This strategy ensures that the cache always holds the most recently added items and discards the oldest ones.

#### Implementing FIFO Caching in Python
We can implement FIFO caching using a Python dictionary and the ``collections.OrderedDict``, which maintains the order of insertion. When the cache limit is reached, we simply remove the first item added (the "first in").
```python
from collections import OrderedDict

class FIFOCache:
    def __init__(self, capacity: int):
        self.capacity = capacity  # Maximum number of items in cache
        self.cache = OrderedDict()  # Ordered dictionary to store cache items

    def put(self, key, value):
        if key in self.cache:
            # If the key is already in the cache, remove it to update the order
            self.cache.pop(key)
        elif len(self.cache) >= self.capacity:
            # FIFO: Remove the oldest item from the cache (first item added)
            self.cache.popitem(last=False)
        # Add the new item to the cache
        self.cache[key] = value

    def get(self, key):
        # Return the value if the key is in cache, else return None
        return self.cache.get(key, None)

    def display(self):
        # Display the current cache state for easy inspection
        print("Cache:", self.cache)

# Usage
fifo_cache = FIFOCache(capacity=3)
fifo_cache.put("a", 1)
fifo_cache.put("b", 2)
fifo_cache.put("c", 3)
fifo_cache.display()  # Cache: OrderedDict([('a', 1), ('b', 2), ('c', 3)])

# Adding another item causes the oldest item ('a') to be evicted
fifo_cache.put("d", 4)
fifo_cache.display()  # Cache: OrderedDict([('b', 2), ('c', 3), ('d', 4)])

print(fifo_cache.get("b"))  # Output: 2
print(fifo_cache.get("a"))  # Output: None (since 'a' was evicted)
```
#### Key Points
- The ``OrderedDict`` ensures that items maintain the insertion order.
- By setting ``last=False`` in ``popitem()``, the oldest item (the first inserted) is removed, implementing the FIFO behavior.

This FIFO cache is ideal when we need to maintain order and only want the most recent entries.
</details>
<details>
<summary>What LIFO means</summary>

### LIFO (Last In, First Out)
**LIFO (Last In, First Out)** caching is a caching strategy where the most recently added item is removed first when the cache reaches its maximum size. This is the opposite of FIFO, meaning the "last in" item is the "first out."

#### Implementing LIFO Caching in Python
We can use a standard dictionary along with a list to track insertion order, where the latest entry is removed when the cache exceeds its limit.
```python
class LIFOCache:
    def __init__(self, capacity: int):
        self.capacity = capacity  # Maximum number of items in cache
        self.cache = {}  # Dictionary to store cache items
        self.order = []  # List to keep track of insertion order

    def put(self, key, value):
        if key in self.cache:
            # If the key already exists, update its value and refresh its position
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            # LIFO: Remove the most recently added item
            last_in_key = self.order.pop()
            del self.cache[last_in_key]
        # Add the new item to the cache and update the order list
        self.cache[key] = value
        self.order.append(key)

    def get(self, key):
        # Return the value if the key is in cache, else return None
        return self.cache.get(key, None)

    def display(self):
        # Display the current cache state for easy inspection
        print("Cache:", self.cache)

# Usage
lifo_cache = LIFOCache(capacity=3)
lifo_cache.put("a", 1)
lifo_cache.put("b", 2)
lifo_cache.put("c", 3)
lifo_cache.display()  # Cache: {'a': 1, 'b': 2, 'c': 3}

# Adding another item causes the most recent item ('c') to be evicted
lifo_cache.put("d", 4)
lifo_cache.display()  # Cache: {'a': 1, 'b': 2, 'd': 4}

print(lifo_cache.get("b"))  # Output: 2
print(lifo_cache.get("c"))  # Output: None (since 'c' was evicted)
```
#### Key Points
- ``order`` **List**: Tracks insertion order, with the last entry representing the most recently added item.
- The **LIFO behavior** is achieved by removing the last item in ``order`` when the cache reaches capacity.

This LIFO cache is ideal when you want to evict the most recently added items first, such as in certain stack-like operations or rollback systems.
</details>
<details>
<summary>What LRU means</summary>

### LRU (Least Recently Used)
**LRU (Least Recently Used)** caching is a strategy where the item that hasn’t been accessed for the longest time is evicted when the cache reaches its maximum capacity. This approach prioritizes keeping frequently or recently accessed items in the cache and discards those that are rarely used.

In Python, ``OrderedDict`` from the ``collections`` module is perfect for implementing an LRU cache, as it maintains the order of keys based on insertion or recent access when we rearrange items.
#### Implementing LRU Caching in Python
We can achieve an LRU cache by:

Moving accessed items to the end of the cache (most recent position).
Removing the least-recently accessed item (at the start of the cache) when we reach the cache's maximum size.
```python
from collections import OrderedDict

class LRUCache(OrderedDict):
    def __init__(self, capacity: int):
        super().__init__()
        self.capacity = capacity  # Maximum number of items in cache

    def put(self, key, value):
        # If the key is already in cache, move it to the end (most recent)
        if key in self:
            self.move_to_end(key)
        # Add/Update the key-value pair
        self[key] = value
        # If cache exceeds capacity, remove the oldest item (first item)
        if len(self) > self.capacity:
            self.popitem(last=False)  # Remove the least recently used item

    def get(self, key):
        # If key is found, move it to the end (most recent) and return its value
        if key in self:
            self.move_to_end(key)
            return self[key]
        # If key not found, return None
        return None

    def display(self):
        # Display the current cache state for easy inspection
        print("Cache:", self)

# Usage
lru_cache = LRUCache(capacity=3)
lru_cache.put("a", 1)
lru_cache.put("b", 2)
lru_cache.put("c", 3)
lru_cache.display()  # Cache: LRUCache([('a', 1), ('b', 2), ('c', 3)])

# Accessing 'a' to make it the most recently used
print(lru_cache.get("a"))  # Output: 1
lru_cache.display()  # Cache: LRUCache([('b', 2), ('c', 3), ('a', 1)])

# Adding a new item causes the least recently used ('b') to be evicted
lru_cache.put("d", 4)
lru_cache.display()  # Cache: LRUCache([('c', 3), ('a', 1), ('d', 4)])
```
#### Why OrderedDict Works Well for LRU
- Order Preservation: ``OrderedDict`` maintains the insertion order, and by using ``move_to_end()``, we can control which items are most or least recent.
- Efficient Access and Update: Both ``move_to_end()`` and ``popitem(last=False)`` make it easy to update or evict items with minimal additional code.

This approach is efficient, clean, and leverages Python’s built-in data structures for an effective LRU cache.
</details>
<details>
<summary>What MRU means</summary>

### MRU (Most Recently Used)
MRU (Most Recently Used) caching is a strategy where the most recently accessed item is removed first when the cache reaches its maximum capacity. This is the opposite of **LRU**: rather than evicting the least recently accessed item, MRU evicts the most recently accessed item.

#### Implementing MRU Caching in Python
For MRU caching, we can use ``OrderedDict`` similarly to LRU, but instead of removing the least recently accessed item, we remove the **most recent** item when we reach the cache's capacity.
```python
from collections import OrderedDict

class MRUCache(OrderedDict):
    def __init__(self, capacity: int):
        super().__init__()
        self.capacity = capacity  # Maximum number of items in cache

    def put(self, key, value):
        # If key already in cache, move it to the end to mark as most recent
        if key in self:
            self.move_to_end(key)
        # Add or update the key-value pair in cache
        self[key] = value
        # If cache exceeds capacity, remove the most recent item
        if len(self) > self.capacity:
            self.popitem(last=True)  # Remove the most recently used item

    def get(self, key):
        # If key is found, move it to the end to mark as most recent and return its value
        if key in self:
            self.move_to_end(key)
            return self[key]
        # If key not found, return None
        return None

    def display(self):
        # Display the current cache state for easy inspection
        print("Cache:", self)

# Usage
mru_cache = MRUCache(capacity=3)
mru_cache.put("a", 1)
mru_cache.put("b", 2)
mru_cache.put("c", 3)
mru_cache.display()  # Cache: MRUCache([('a', 1), ('b', 2), ('c', 3)])

# Accessing 'c' to make it the most recently used
print(mru_cache.get("c"))  # Output: 3
mru_cache.display()  # Cache: MRUCache([('a', 1), ('b', 2), ('c', 3)])

# Adding a new item causes the most recently used ('c') to be evicted
mru_cache.put("d", 4)
mru_cache.display()  # Cache: MRUCache([('a', 1), ('b', 2), ('d', 4)])
```
#### Key Points
- MRU caching is useful in situations where recently accessed data is likely to be discarded soon, such as temporary files or redundant, short-term data.
- To implement MRU in ``OrderedDict``, ``popitem(last=True)`` removes the most recently accessed item when the cache is full
- Capacity Management: When the cache limit is exceeded, the most recent item is removed to maintain capacity.

</details>
<details>
<summary>What LFU means</summary>

### LFU (Least Frequently Used)
LFU (Least Frequently Used) caching is a strategy that evicts the least frequently accessed items when the cache reaches its maximum capacity. It prioritizes retaining items that are accessed more often, assuming that items used frequently will likely be used again soon.
#### Key Points of LFU:
**1. Definition: Least Frequently Used (LFU)** caching evicts the item that has been accessed the least often, ensuring that frequently accessed items remain in the cache.
**2. Use Case:** LFU caching is beneficial in scenarios where access patterns vary significantly, such as in caching user preferences or popular content, where some items are accessed much more frequently than others.
**3. Eviction Strategy:** When the cache exceeds its capacity, the item with the lowest access frequency is evicted. If there are ties, the item that was added first among the least frequently used items can be evicted.
**4. Data Structure:** To implement LFU, you typically use a dictionary to store cached items along with their access counts and a secondary structure (like a min-heap or an OrderedDict) to manage the items by frequency of access.
#### Implementing LFU Caching in Python
```python
class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # Store key-value pairs
        self.freq = {}   # Store frequency counts for each key
        self.min_freq = 0  # Track the minimum frequency of access
        self.usage_order = {}  # Store keys in order of frequency

    def get(self, key):
        if key not in self.cache:
            return None  # Key not found
        # Update frequency
        self.freq[key] += 1
        freq = self.freq[key]

        # Update usage order
        if freq - 1 in self.usage_order:
            self.usage_order[freq - 1].remove(key)
            if not self.usage_order[freq - 1]:
                del self.usage_order[freq - 1]

        # Add key to the new frequency list
        if freq in self.usage_order:
            self.usage_order[freq].append(key)
        else:
            self.usage_order[freq] = [key]

        # Update minimum frequency if needed
        if freq - 1 == self.min_freq and freq - 1 not in self.usage_order:
            self.min_freq += 1

        return self.cache[key]

    def put(self, key, value):
        if self.capacity == 0:
            return  # No capacity, do nothing

        if key in self.cache:
            self.cache[key] = value
            self.get(key)  # Update frequency on access
            return

        if len(self.cache) >= self.capacity:
            # Evict the least frequently used item
            lfu_key = self.usage_order[self.min_freq].pop(0)
            del self.cache[lfu_key]
            del self.freq[lfu_key]
            if not self.usage_order[self.min_freq]:
                del self.usage_order[self.min_freq]

        # Insert new key-value pair
        self.cache[key] = value
        self.freq[key] = 1  # New item accessed once
        self.min_freq = 1
        self.usage_order.setdefault(1, []).append(key)

# Usage
lfu_cache = LFUCache(capacity=3)
lfu_cache.put("a", 1)
lfu_cache.put("b", 2)
lfu_cache.put("c", 3)

print(lfu_cache.get("a"))  # Access 'a', frequency increases
lfu_cache.put("d", 4)  # Evicts the least frequently used item
print(lfu_cache.get("b"))  # Output: 2
```
#### Explanation
##### 1. Data Structures:
- ``cache``: A dictionary to store key-value pairs.
- ``freq``: A dictionary to track how many times each key has been accessed.
- ``usage_order``: A dictionary to store keys grouped by their access frequency, allowing efficient eviction of the least frequently used items.
- ``min_freq``: Tracks the minimum frequency of access to identify which items to evict.
##### 2. ``get(key)`` Method:
If the key is found in the cache, it updates the access frequency and manages the ``usage_order``. If the key is not found, it returns ``None``.
##### 3. ``put(key, value)`` Method:
- If the key already exists, it updates the value and refreshes its frequency.
- If the key does not exist and the cache is full, it evicts the least frequently used item based on the current minimum frequency before adding the new item.
#### Summary
- **LFU Caching:** Evicts the least frequently accessed item when the cache is full, prioritizing frequently accessed items.
- **Implementation Complexity:** Requires managing both the cached items and their access frequencies, leading to more complex logic than simpler caching strategies like LRU or MRU.
- **Usefulness:** Effective in managing caches where some items are accessed much more frequently than others, ensuring popular data stays available.
</details>
<details>
<summary>What limits a caching system have</summary>

### Caching Systems Limitations
Caching systems have several limitations and challenges that can affect their effectiveness and usability:
#### 1. Cache Size:
Limited storage capacity can restrict the amount of data that can be cached, leading to potential evictions of frequently used items or less popular data not being cached at all.

#### 2. Data Staleness:
Cached data can become outdated if the underlying data changes. This can lead to inconsistencies between the cached data and the source of truth, especially in environments with high data churn.

#### 3. Cache Misses:
A cache miss occurs when requested data is not found in the cache, necessitating a retrieval from the original source, which can negate the performance benefits of caching.

#### 4. Complexity of Cache Management:
Implementing an effective caching strategy can be complex. Decisions about when to cache data, how long to keep it, and which eviction strategy to use (e.g., LRU, LFU, FIFO) require careful consideration.

#### 5. Cost:
While caching can reduce costs related to data retrieval, the infrastructure needed to implement caching (e.g., dedicated cache servers or services) can incur additional costs, especially at scale.

#### 6. Concurrency Issues:
In multi-threaded or distributed environments, managing concurrent access to cache can lead to race conditions or data corruption if not handled properly.

#### 7. Overhead:
The process of adding caching layers introduces some overhead in terms of complexity, maintenance, and potential performance bottlenecks if the cache layer itself becomes a point of contention.

#### 8. Increased Latency for Cache Updates:
Updating cached data can introduce latency, particularly if cache invalidation is not handled efficiently. It may be necessary to implement complex invalidation strategies to ensure that users always see the most current data.

#### 9. Application-Specific:
ing strategies and implementations often need to be tailored to specific applications or workloads, which can limit the generalizability of caching solutions across different systems.

#### 10. Limited by Data Access Patterns:
The effectiveness of a caching system is highly dependent on the data access patterns. If access patterns are unpredictable or vary significantly, the cache may not be able to provide substantial benefits.

In summary, while caching systems can significantly improve performance and reduce load on backend systems, they also come with limitations that require careful consideration and management to maximize their effectiveness.
</details>

## More Info
### Parent class ``BaseCaching``
All your classes must inherit from ``BaseCaching`` defined below:
```bash
$ cat base_caching.py
#!/usr/bin/python3
""" BaseCaching module
"""

class BaseCaching():
    """ BaseCaching defines:
      - constants of your caching system
      - where your data are stored (in a dictionary)
    """
    MAX_ITEMS = 4

    def __init__(self):
        """ Initiliaze
        """
        self.cache_data = {}

    def print_cache(self):
        """ Print the cache
        """
        print("Current cache:")
        for key in sorted(self.cache_data.keys()):
            print("{}: {}".format(key, self.cache_data.get(key)))

    def put(self, key, item):
        """ Add an item in the cache
        """
        raise NotImplementedError("put must be implemented in your cache class")

    def get(self, key):
        """ Get an item by key
        """
        raise NotImplementedError("get must be implemented in your cache class")
```
## Tasks
### 0. Basic dictionary
Create a class ``BasicCache`` that inherits from ``BaseCaching`` and is a caching system:
- You must use ``self.cache_data`` - dictionary from the parent class ``BaseCaching``
- This caching system doesn’t have limit
- ``def put(self, key, item):``
    + Must assign to the dictionary ``self.cache_data`` the ``item`` value for the key ``key``.
    + If ``key`` or ``item`` is ``None``, this method should not do anything.
- ``def get(self, key):``
    + Must return the value in ``self.cache_data`` linked to ``key``.
    + If ``key`` is ``None`` or if the ``key`` doesn’t exist in ``self.cache_data``, return ``None``.
```bash
$ cat 0-main.py
#!/usr/bin/python3
""" 0-main """
BasicCache = __import__('0-basic_cache').BasicCache

my_cache = BasicCache()
my_cache.print_cache()
my_cache.put("A", "Hello")
my_cache.put("B", "World")
my_cache.put("C", "Holberton")
my_cache.print_cache()
print(my_cache.get("A"))
print(my_cache.get("B"))
print(my_cache.get("C"))
print(my_cache.get("D"))
my_cache.print_cache()
my_cache.put("D", "School")
my_cache.put("E", "Battery")
my_cache.put("A", "Street")
my_cache.print_cache()
print(my_cache.get("A"))

$ ./0-main.py
Current cache:
Current cache:
A: Hello
B: World
C: Holberton
Hello
World
Holberton
None
Current cache:
A: Hello
B: World
C: Holberton
Current cache:
A: Street
B: World
C: Holberton
D: School
E: Battery
Street
```
### 1. FIFO caching
Create a class ``FIFOCache`` that inherits from ``BaseCaching`` and is a caching system:
- You must use ``self.cache_data`` - dictionary from the parent class ``BaseCaching``
- You can overload ``def __init__(self):`` but don’t forget to call the parent init: ``super().__init__()``
- ``def put(self, key, item):``
    + Must assign to the dictionary ``self.cache_data`` the item value for the key ``key``.
    + If ``key`` or ``item`` is ``None``, this method should not do anything.
    + If the number of items in ``self.cache_data`` is higher that ``BaseCaching.MAX_ITEMS``:
        - you must discard the first item put in cache (FIFO algorithm)
        - you must print ``DISCARD``: with the ``key`` discarded and following by a new line
- ``def get(self, key):``
    + Must return the value in ``self.cache_data`` linked to ``key``.
    + If ``key`` is ``None`` or if the ``key`` doesn’t exist in ``self.cache_data``, return ``None``.
```bash
$ cat 1-main.py
#!/usr/bin/python3
""" 1-main """
FIFOCache = __import__('1-fifo_cache').FIFOCache

my_cache = FIFOCache()
my_cache.put("A", "Hello")
my_cache.put("B", "World")
my_cache.put("C", "Holberton")
my_cache.put("D", "School")
my_cache.print_cache()
my_cache.put("E", "Battery")
my_cache.print_cache()
my_cache.put("C", "Street")
my_cache.print_cache()
my_cache.put("F", "Mission")
my_cache.print_cache()

$ ./1-main.py
Current cache:
A: Hello
B: World
C: Holberton
D: School
DISCARD: A
Current cache:
B: World
C: Holberton
D: School
E: Battery
Current cache:
B: World
C: Street
D: School
E: Battery
DISCARD: B
Current cache:
C: Street
D: School
E: Battery
F: Mission
``` 
### 2. LIFO Caching
Create a class ``LIFOCache`` that inherits from ``BaseCaching`` and is a caching system:
- You must use ``self.cache_data`` - dictionary from the parent class ``BaseCaching``
- You can overload ``def __init__(self):`` but don’t forget to call the parent init: ``super().__init__()``
- ``def put(self, key, item):``
    + Must assign to the dictionary ``self.cache_data`` the ``item`` value for the key ``key``.
    + If ``key`` or ``item`` is ``None``, this method should not do anything.
    + If the number of items in ``self.cache_data`` is higher that ``BaseCaching.MAX_ITEMS``:
        - you must discard the last item put in cache (LIFO algorithm)
        - you must print ``DISCARD``: with the ``key`` discarded and following by a new line
- ``def get(self, key):``
    + Must return the value in ``self.cache_data`` linked to ``key``.
    + If ``key`` is ``None`` or if the ``key`` doesn’t exist in ``self.cache_data``, return ``None``.
```bash
$ cat 2-main.py
#!/usr/bin/python3
""" 2-main """
LIFOCache = __import__('2-lifo_cache').LIFOCache

my_cache = LIFOCache()
my_cache.put("A", "Hello")
my_cache.put("B", "World")
my_cache.put("C", "Holberton")
my_cache.put("D", "School")
my_cache.print_cache()
my_cache.put("E", "Battery")
my_cache.print_cache()
my_cache.put("C", "Street")
my_cache.print_cache()
my_cache.put("F", "Mission")
my_cache.print_cache()
my_cache.put("G", "San Francisco")
my_cache.print_cache()

$ ./2-main.py
Current cache:
A: Hello
B: World
C: Holberton
D: School
DISCARD: D
Current cache:
A: Hello
B: World
C: Holberton
E: Battery
Current cache:
A: Hello
B: World
C: Street
E: Battery
DISCARD: C
Current cache:
A: Hello
B: World
E: Battery
F: Mission
DISCARD: F
Current cache:
A: Hello
B: World
E: Battery
G: San Francisco
```
### 3. LRU Caching
Create a class ``LRUCache`` that inherits from ``BaseCaching`` and is a caching system:
- You must use ``self.cache_data`` - dictionary from the parent class ``BaseCaching``
- You can overload ``def __init__(self):`` but don’t forget to call the parent init: ``super().__init__()``
- ``def put(self, key, item):``
    + Must assign to the dictionary ``self.cache_data`` the ``item`` value for the key ``key``.
    + If ``key`` or ``item`` is ``None``, this method should not do anything.
    + If the number of items in ``self.cache_data`` is higher that ``BaseCaching.MAX_ITEMS``:
        - you must discard the least recently used item (LRU algorithm)
        - you must print ``DISCARD``: with the ``key`` discarded and following by a new line
- ``def get(self, key):``
    + Must return the value in ``self.cache_data`` linked to ``key``.
    + If ``key`` is ``None`` or if the ``key`` doesn’t exist in ``self.cache_data``, return ``None``.
```bash
$ cat 3-main.py
#!/usr/bin/python3
""" 3-main """
LRUCache = __import__('3-lru_cache').LRUCache

my_cache = LRUCache()
my_cache.put("A", "Hello")
my_cache.put("B", "World")
my_cache.put("C", "Holberton")
my_cache.put("D", "School")
my_cache.print_cache()
print(my_cache.get("B"))
my_cache.put("E", "Battery")
my_cache.print_cache()
my_cache.put("C", "Street")
my_cache.print_cache()
print(my_cache.get("A"))
print(my_cache.get("B"))
print(my_cache.get("C"))
my_cache.put("F", "Mission")
my_cache.print_cache()
my_cache.put("G", "San Francisco")
my_cache.print_cache()
my_cache.put("H", "H")
my_cache.print_cache()
my_cache.put("I", "I")
my_cache.print_cache()
my_cache.put("J", "J")
my_cache.print_cache()
my_cache.put("K", "K")
my_cache.print_cache()

$ ./3-main.py
Current cache:
A: Hello
B: World
C: Holberton
D: School
World
DISCARD: A
Current cache:
B: World
C: Holberton
D: School
E: Battery
Current cache:
B: World
C: Street
D: School
E: Battery
None
World
Street
DISCARD: D
Current cache:
B: World
C: Street
E: Battery
F: Mission
DISCARD: E
Current cache:
B: World
C: Street
F: Mission
G: San Francisco
DISCARD: B
Current cache:
C: Street
F: Mission
G: San Francisco
H: H
DISCARD: C
Current cache:
F: Mission
G: San Francisco
H: H
I: I
DISCARD: F
Current cache:
G: San Francisco
H: H
I: I
J: J
DISCARD: G
Current cache:
H: H
I: I
J: J
K: K
```
### 4. MRU Caching
Create a class ``MRUCache`` that inherits from ``BaseCaching`` and is a caching system:
- You must use ``self.cache_data`` - dictionary from the parent class ``BaseCaching``
- You can overload ``def __init__(self):`` but don’t forget to call the parent init: ``super().__init__()``
- ``def put(self, key, item):``
    + Must assign to the dictionary ``self.cache_data`` the ``item`` value for the key ``key``.
    + If ``key`` or ``item`` is ``None``, this method should not do anything.
    + If the number of items in ``self.cache_data`` is higher that ``BaseCaching.MAX_ITEMS``:
        - you must discard the most recently used item (MRU algorithm)
        - you must print ``DISCARD``: with the ``key`` discarded and following by a new line
- ``def get(self, key):``
    + Must return the value in ``self.cache_data`` linked to ``key``.
    + If ``key`` is ``None`` or if the ``key`` doesn’t exist in ``self.cache_data``, return ``None``.
```bash
$ cat 4-main.py
#!/usr/bin/python3
""" 4-main """
MRUCache = __import__('4-mru_cache').MRUCache

my_cache = MRUCache()
my_cache.put("A", "Hello")
my_cache.put("B", "World")
my_cache.put("C", "Holberton")
my_cache.put("D", "School")
my_cache.print_cache()
print(my_cache.get("B"))
my_cache.put("E", "Battery")
my_cache.print_cache()
my_cache.put("C", "Street")
my_cache.print_cache()
print(my_cache.get("A"))
print(my_cache.get("B"))
print(my_cache.get("C"))
my_cache.put("F", "Mission")
my_cache.print_cache()
my_cache.put("G", "San Francisco")
my_cache.print_cache()
my_cache.put("H", "H")
my_cache.print_cache()
my_cache.put("I", "I")
my_cache.print_cache()
my_cache.put("J", "J")
my_cache.print_cache()
my_cache.put("K", "K")
my_cache.print_cache()

$ ./4-main.py
Current cache:
A: Hello
B: World
C: Holberton
D: School
World
DISCARD: B
Current cache:
A: Hello
C: Holberton
D: School
E: Battery
Current cache:
A: Hello
C: Street
D: School
E: Battery
Hello
None
Street
DISCARD: C
Current cache:
A: Hello
D: School
E: Battery
F: Mission
DISCARD: F
Current cache:
A: Hello
D: School
E: Battery
G: San Francisco
DISCARD: G
Current cache:
A: Hello
D: School
E: Battery
H: H
DISCARD: H
Current cache:
A: Hello
D: School
E: Battery
I: I
DISCARD: I
Current cache:
A: Hello
D: School
E: Battery
J: J
DISCARD: J
Current cache:
A: Hello
D: School
E: Battery
K: K
```
### 5. LFU Caching
Create a class ``LFUCache`` that inherits from ``BaseCaching`` and is a caching system:
- You must use ``self.cache_data`` - dictionary from the parent class ``BaseCaching``
- You can overload ``def __init__(self):`` but don’t forget to call the parent init: ``super().__init__()``
- ``def put(self, key, item):``
    + Must assign to the dictionary ``self.cache_data`` the ``item`` value for the key ``key``.
    + If ``key`` or ``item`` is ``None``, this method should not do anything.
    + If the number of items in ``self.cache_data`` is higher that ``BaseCaching.MAX_ITEMS``:
        - you must discard the least frequency used item (LFU algorithm)
        - if you find more than 1 item to discard, you must use the LRU algorithm to discard only the least recently used
        - you must print ``DISCARD``: with the ``key`` discarded and following by a new line
- ``def get(self, key):``
    + Must return the value in ``self.cache_data`` linked to ``key``.
    + If ``key`` is ``None`` or if the ``key`` doesn’t exist in ``self.cache_data``, return ``None``.
```bash
$ cat 100-main.py
#!/usr/bin/python3
""" 100-main """
LFUCache = __import__('100-lfu_cache').LFUCache

my_cache = LFUCache()
my_cache.put("A", "Hello")
my_cache.put("B", "World")
my_cache.put("C", "Holberton")
my_cache.put("D", "School")
my_cache.print_cache()
print(my_cache.get("B"))
my_cache.put("E", "Battery")
my_cache.print_cache()
my_cache.put("C", "Street")
my_cache.print_cache()
print(my_cache.get("A"))
print(my_cache.get("B"))
print(my_cache.get("C"))
my_cache.put("F", "Mission")
my_cache.print_cache()
my_cache.put("G", "San Francisco")
my_cache.print_cache()
my_cache.put("H", "H")
my_cache.print_cache()
my_cache.put("I", "I")
my_cache.print_cache()
print(my_cache.get("I"))
print(my_cache.get("H"))
print(my_cache.get("I"))
print(my_cache.get("H"))
print(my_cache.get("I"))
print(my_cache.get("H"))
my_cache.put("J", "J")
my_cache.print_cache()
my_cache.put("K", "K")
my_cache.print_cache()
my_cache.put("L", "L")
my_cache.print_cache()
my_cache.put("M", "M")
my_cache.print_cache()

$ ./100-main.py
Current cache:
A: Hello
B: World
C: Holberton
D: School
World
DISCARD: A
Current cache:
B: World
C: Holberton
D: School
E: Battery
Current cache:
B: World
C: Street
D: School
E: Battery
None
World
Street
DISCARD: D
Current cache:
B: World
C: Street
E: Battery
F: Mission
DISCARD: E
Current cache:
B: World
C: Street
F: Mission
G: San Francisco
DISCARD: F
Current cache:
B: World
C: Street
G: San Francisco
H: H
DISCARD: G
Current cache:
B: World
C: Street
H: H
I: I
I
H
I
H
I
H
DISCARD: B
Current cache:
C: Street
H: H
I: I
J: J
DISCARD: J
Current cache:
C: Street
H: H
I: I
K: K
DISCARD: K
Current cache:
C: Street
H: H
I: I
L: L
DISCARD: L
Current cache:
C: Street
H: H
I: I
M: M
