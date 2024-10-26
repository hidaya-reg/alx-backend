#!/usr/bin/env python3
"""
Simple helper function
"""


def index_range(page, page_size):
    """
        function that returns a tuple of size two containing
        a start index and an end index corresponding to the range of indexes
    """
    start = (page - 1) * page_size
    end = page * page_size
    return (start, end)
