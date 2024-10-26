# 0x00. Pagination
## Resources
- [REST API Design: Pagination](https://www.moesif.com/blog/technical/api-design/REST-API-Design-Filtering-Sorting-and-Pagination/#pagination)
- [HATEOAS](https://www.youtube.com/watch?v=gCNAudrbWCo)

## Learning Objectives
<details>
<summary>How to paginate a dataset with simple `page` and `page_size` parameters</summary>

To paginate a dataset with simple ``page`` and ``page_size`` parameters, you determine the range of items to return based on the page number and the number of items per page.`
- For ``page=1`` and ``page_size=10``, you would return items from index 0 to 9.
- For ``page=2`` and ``page_size=10``, you would return items from index 10 to 19.
The start index is calculated as ``(page - 1) * page_size``, and the end index is ``page * page_size``.

```python
def index_range(page, page_size):
    start = (page - 1) * page_size
    end = page * page_size
    return (start, end)

# Example usage:
print(index_range(1, 10))  # Output: (0, 10)
print(index_range(2, 10))  # Output: (10, 20)
```
</details>
<details>
<summary>How to paginate a dataset with hypermedia metadata</summary>

To paginate a dataset with hypermedia metadata, you include additional information in the response that guides the client on how to navigate the pages. This typically includes the current page, page size, total pages, and links to the next and previous pages.

**Example:** Imagine you have a dataset of 50 items, and you are returning 10 items per page. Along with the data for the current page, you would also return metadata like this:

```python
def paginate_with_hypermedia(page, page_size, total_items):
    total_pages = (total_items + page_size - 1) // page_size
    data = dataset[(page - 1) * page_size: page * page_size]
    
    return {
        "page": page,
        "page_size": len(data),
        "data": data,
        "next_page": page + 1 if page < total_pages else None,
        "prev_page": page - 1 if page > 1 else None,
        "total_pages": total_pages
    }

# Example usage:
print(paginate_with_hypermedia(1, 10, 50))
# Output:
# {
#   "page": 1,
#   "page_size": 10,
#   "data": [...],  # Items 0-9
#   "next_page": 2,
#   "prev_page": None,
#   "total_pages": 5
# }
```
This method provides not only the data for the current page but also the necessary metadata to navigate through the dataset easily.
</details>
<details>
<summary>How to paginate in a deletion-resilient manner</summary>

Paginating in a deletion-resilient manner means ensuring that users don’t miss any items in a dataset even if some items are deleted between pagination requests. This is typically done by keeping track of the indices of items rather than just the page numbers.

**Example:**
Imagine you have a dataset with 10 items and you're showing 3 items per page. Normally, if you delete an item, the items on the next page might shift, causing users to miss some data.

To avoid this, you could index the dataset before pagination and use the indices to fetch data, even if items are removed.
```python
class Server:
    def __init__(self, dataset):
        self.dataset = dataset
        self.indexed_dataset = {i: item for i, item in enumerate(dataset)}

    def get_hyper_index(self, index, page_size):
        data = []
        next_index = index
        while len(data) < page_size and next_index in self.indexed_dataset:
            data.append(self.indexed_dataset[next_index])
            next_index += 1

        return {
            "index": index,
            "data": data,
            "page_size": len(data),
            "next_index": next_index if next_index in self.indexed_dataset else None
        }

# Example usage:
dataset = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
server = Server(dataset)

# Deleting some items
del server.indexed_dataset[3]  # Deletes "d"
del server.indexed_dataset[5]  # Deletes "f"

# Fetching the first page (3 items starting from index 2)
print(server.get_hyper_index(2, 3))
# Output:
# {
#   "index": 2,
#   "data": ["c", "e", "g"],  # "d" and "f" were skipped because they were deleted
#   "page_size": 3,
#   "next_index": 6
# }
```
**Explanation:**
- Indexed Dataset: The dataset is first indexed so that each item has a unique index.
- Deletion: Even if some items are deleted, the remaining items can still be paginated without skipping over any items or showing empty pages.
- get_hyper_index: This method fetches the data based on the current index and adjusts for any deletions, ensuring a consistent pagination experience.
</details>



## Setup: `Popular_Baby_Names.csv`
Use this data file for your project.

## Tasks

### 0. Simple helper function

Write a function named `index_range` that takes two integer arguments `page` and `page_size`.

- The function should return a tuple of size two containing a start index and an end index corresponding to the range of indexes to return in a list for those particular pagination parameters.
- Page numbers are 1-indexed, i.e., the first page is page 1.


```bash
$ cat 0-main.py
#!/usr/bin/env python3
"""
Main file
"""

index_range = __import__('0-simple_helper_function').index_range

res = index_range(1, 7)
print(type(res))
print(res)

res = index_range(page=3, page_size=15)
print(type(res))
print(res)

$ ./0-main.py
<class 'tuple'>
(0, 7)
<class 'tuple'>
(30, 45)
$
```
### 1. Simple pagination

Copy ``index_range`` from the previous task and the following class into your code
```python
import csv
import math
from typing import List


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
            pass
```
Implement a method named ``get_page`` that takes two integer arguments ``page`` with default value 1 and ``page_size`` with default value 10.

- You have to use this ``CSV file`` (same as the one presented at the top of the project)
- Use ``assert`` to verify that both arguments are integers greater than 0.
- Use ``index_range`` to find the correct indexes to paginate the dataset correctly and return the appropriate page of the dataset (i.e. the correct list of rows).
- If the input arguments are out of range for the dataset, an empty list should be returned.
```bash
$  wc -l Popular_Baby_Names.csv 
19419 Popular_Baby_Names.csv
$  
$ head Popular_Baby_Names.csv
Year of Birth,Gender,Ethnicity,Child's First Name,Count,Rank
2016,FEMALE,ASIAN AND PACIFIC ISLANDER,Olivia,172,1
2016,FEMALE,ASIAN AND PACIFIC ISLANDER,Chloe,112,2
2016,FEMALE,ASIAN AND PACIFIC ISLANDER,Sophia,104,3
2016,FEMALE,ASIAN AND PACIFIC ISLANDER,Emma,99,4
2016,FEMALE,ASIAN AND PACIFIC ISLANDER,Emily,99,4
2016,FEMALE,ASIAN AND PACIFIC ISLANDER,Mia,79,5
2016,FEMALE,ASIAN AND PACIFIC ISLANDER,Charlotte,59,6
2016,FEMALE,ASIAN AND PACIFIC ISLANDER,Sarah,57,7
2016,FEMALE,ASIAN AND PACIFIC ISLANDER,Isabella,56,8
$  cat 1-main.py
#!/usr/bin/env python3
"""
Main file
"""

Server = __import__('1-simple_pagination').Server

server = Server()

try:
    should_err = server.get_page(-10, 2)
except AssertionError:
    print("AssertionError raised with negative values")

try:
    should_err = server.get_page(0, 0)
except AssertionError:
    print("AssertionError raised with 0")

try:
    should_err = server.get_page(2, 'Bob')
except AssertionError:
    print("AssertionError raised when page and/or page_size are not ints")


print(server.get_page(1, 3))
print(server.get_page(3, 2))
print(server.get_page(3000, 100))

$ 
$ ./1-main.py
AssertionError raised with negative values
AssertionError raised with 0
AssertionError raised when page and/or page_size are not ints
[['2016', 'FEMALE', 'ASIAN AND PACIFIC ISLANDER', 'Olivia', '172', '1'], ['2016', 'FEMALE', 'ASIAN AND PACIFIC ISLANDER', 'Chloe', '112', '2'], ['2016', 'FEMALE', 'ASIAN AND PACIFIC ISLANDER', 'Sophia', '104', '3']]
[['2016', 'FEMALE', 'ASIAN AND PACIFIC ISLANDER', 'Emily', '99', '4'], ['2016', 'FEMALE', 'ASIAN AND PACIFIC ISLANDER', 'Mia', '79', '5']]
[]
```
  
### 2. Hypermedia pagination

Replicate code from the previous task.

Implement a ``get_hyper`` method that takes the same arguments (and defaults) as ``get_page`` and returns a dictionary containing the following key-value pairs:

- ``page_size``: the length of the returned dataset page
- ``page``: the current page number
- ``data``: the dataset page (equivalent to return from previous task)
- ``next_page``: number of the next page, None if no next page
- ``prev_page``: number of the previous page, None if no previous page
- ``total_pages``: the total number of pages in the dataset as an integer
Make sure to reuse ``get_page`` in your implementation.

You can use the ``math`` module if necessary.
``` bash
$ cat 2-main.py
#!/usr/bin/env python3
"""
Main file
"""

Server = __import__('2-hypermedia_pagination').Server

server = Server()

print(server.get_hyper(1, 2))
print("---")
print(server.get_hyper(2, 2))
print("---")
print(server.get_hyper(100, 3))
print("---")
print(server.get_hyper(3000, 100))

$ 
$ ./2-main.py
{'page_size': 2, 'page': 1, 'data': [['2016', 'FEMALE', 'ASIAN AND PACIFIC ISLANDER', 'Olivia', '172', '1'], ['2016', 'FEMALE', 'ASIAN AND PACIFIC ISLANDER', 'Chloe', '112', '2']], 'next_page': 2, 'prev_page': None, 'total_pages': 9709}
---
{'page_size': 2, 'page': 2, 'data': [['2016', 'FEMALE', 'ASIAN AND PACIFIC ISLANDER', 'Sophia', '104', '3'], ['2016', 'FEMALE', 'ASIAN AND PACIFIC ISLANDER', 'Emma', '99', '4']], 'next_page': 3, 'prev_page': 1, 'total_pages': 9709}
---
{'page_size': 3, 'page': 100, 'data': [['2016', 'FEMALE', 'BLACK NON HISPANIC', 'Londyn', '14', '39'], ['2016', 'FEMALE', 'BLACK NON HISPANIC', 'Amirah', '14', '39'], ['2016', 'FEMALE', 'BLACK NON HISPANIC', 'McKenzie', '14', '39']], 'next_page': 101, 'prev_page': 99, 'total_pages': 6473}
---
{'page_size': 0, 'page': 3000, 'data': [], 'next_page': None, 'prev_page': 2999, 'total_pages': 195}
```
  
### 3. Deletion-resilient hypermedia pagination

The goal here is that if between two queries, certain rows are removed from the dataset, the user does not miss items from dataset when changing page.

Start ``3-hypermedia_del_pagination.py`` with this code:
```python
#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
            pass
```
Implement a ``get_hyper_index`` method with two integer arguments: ``index`` with a ``None`` default value and ``page_size`` with default value of 10.

- The method should return a dictionary with the following key-value pairs:
	- ``index``: the current start index of the return page. That is the index of the first item in the current page. For example if requesting page 3 with ``page_size`` 20, and no data was removed from the dataset, the current index should be 60.
	- ``next_index``: the next index to query with. That should be the index of the first item after the last item on the current page.
	- ``page_size``: the current page size
	- ``data``: the actual page of the dataset

**Requirements/Behavior:**

- Use ``assert`` to verify that index is in a valid range.
- If the user queries index 0, ``page_size`` 10, they will get rows indexed 0 to 9 included.
- If they request the next index (10) with ``page_size`` 10, but rows 3, 6 and 7 were deleted, the user should still receive rows indexed 10 to 19 included.
```bash
$ cat 3-main.py
#!/usr/bin/env python3
"""
Main file
"""

Server = __import__('3-hypermedia_del_pagination').Server

server = Server()

server.indexed_dataset()

try:
    server.get_hyper_index(300000, 100)
except AssertionError:
    print("AssertionError raised when out of range")        


index = 3
page_size = 2

print("Nb items: {}".format(len(server._Server__indexed_dataset)))

# 1- request first index
res = server.get_hyper_index(index, page_size)
print(res)

# 2- request next index
print(server.get_hyper_index(res.get('next_index'), page_size))

# 3- remove the first index
del server._Server__indexed_dataset[res.get('index')]
print("Nb items: {}".format(len(server._Server__indexed_dataset)))

# 4- request again the initial index -> the first data retreives is not the same as the first request
print(server.get_hyper_index(index, page_size))

# 5- request again initial next index -> same data page as the request 2-
print(server.get_hyper_index(res.get('next_index'), page_size))

$ 
$ ./3-main.py
AssertionError raised when out of range
Nb items: 19418
{'index': 3, 'data': [['2016', 'FEMALE', 'ASIAN AND PACIFIC ISLANDER', 'Emma', '99', '4'], ['2016', 'FEMALE', 'ASIAN AND PACIFIC ISLANDER', 'Emily', '99', '4']], 'page_size': 2, 'next_index': 5}
{'index': 5, 'data': [['2016', 'FEMALE', 'ASIAN AND PACIFIC ISLANDER', 'Mia', '79', '5'], ['2016', 'FEMALE', 'ASIAN AND PACIFIC ISLANDER', 'Charlotte', '59', '6']], 'page_size': 2, 'next_index': 7}
Nb items: 19417
{'index': 3, 'data': [['2016', 'FEMALE', 'ASIAN AND PACIFIC ISLANDER', 'Emily', '99', '4'], ['2016', 'FEMALE', 'ASIAN AND PACIFIC ISLANDER', 'Mia', '79', '5']], 'page_size': 2, 'next_index': 6}
{'index': 5, 'data': [['2016', 'FEMALE', 'ASIAN AND PACIFIC ISLANDER', 'Mia', '79', '5'], ['2016', 'FEMALE', 'ASIAN AND PACIFIC ISLANDER', 'Charlotte', '59', '6']], 'page_size': 2, 'next_index': 7}
```