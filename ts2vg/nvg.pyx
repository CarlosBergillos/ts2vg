#cython: language_level=3

import numpy as np
cimport numpy as np
cimport cython
from numpy.math cimport INFINITY
from ts2vg.pairqueue cimport PairQueue

ctypedef unsigned int uint


@cython.boundscheck(False)
@cython.wraparound(False)
cdef uint _argmax(np.float64_t[:] a, uint left, uint right):
    """Get the argmax of a"""
    cdef uint i
    cdef uint idx = left
    cdef float val = a[left]

    for i in range(left+1, right):
        if a[i] > val:
            val = a[i]
            idx = i
    return idx


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def nvg_edges(np.float64_t[:] ts):
    """
    Computes the visibility graph of a time series
    using a divide-and-conquer strategy and
    returns its edge list.

    Args:
        ts (numpy 1d array): Time series data.

    Returns:
        g (igraph.Graph): The visibility graph of `ts`.
    """
    cdef uint n = ts.size
    edges = []

    cdef uint left, right, i, d
    cdef float y_i, y_a
    cdef float max_slope, slope
    
    cdef PairQueue queue = PairQueue()
    queue.push((0, n))
    
    while not queue.is_empty():
        (left, right) = queue.pop()
        
        if left+1 < right:
            i = _argmax(ts, left, right)
            y_i = ts[i]
            
            max_slope = -INFINITY
            for d in range(1, i-left+1):
                y_a = ts[i-d]
                slope = (y_a-y_i) / d # d = a-i
                if slope > max_slope:
                    edges.append((i, i-d))
                    max_slope = slope
                    
            max_slope = -INFINITY
            for d in range(1, right-i):
                y_a = ts[i+d]
                slope = (y_a-y_i) / d # d = a-i
                if slope > max_slope:
                    edges.append((i, i+d))
                    max_slope = slope

            queue.push((left, i))
            queue.push((i+1, right))
    
    return edges


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def nvg_degrees(np.float64_t[:] ts):
    """
    Computes the degree sequence of the visibility graph
    of a time series.
    The whole graph is not stored in memory, this method
    is more time and memory efficient than calling `visibility_graph`.

    Args:
        ts (numpy 1d array): Time series data.

    Returns:
        g (igraph.Graph): The visibility graph of `ts`.
    """
    cdef uint n = ts.size
    
    cdef uint left, right, i, d
    cdef float y_i, y_a
    cdef float max_slope, slope
    
    cdef np.uint32_t[:] degrees = np.zeros(n, dtype=np.uint32)
    
    cdef PairQueue queue = PairQueue()
    queue.push((0, n))
    
    while not queue.is_empty():
        (left, right) = queue.pop()
        
        if left+1 < right:
            i = _argmax(ts, left, right)
            y_i = ts[i]
            
            max_slope = -INFINITY
            for d in range(1, i-left+1):
                y_a = ts[i-d]
                slope = (y_a-y_i) / d # d = a-i
                if slope > max_slope:
                    degrees[i] += 1
                    degrees[i-d] += 1
                    max_slope = slope
                    
            max_slope = -INFINITY
            for d in range(1, right-i):
                y_a = ts[i+d]
                slope = (y_a-y_i) / d # d = a-i
                if slope > max_slope:
                    degrees[i] += 1
                    degrees[i+d] += 1
                    max_slope = slope

            queue.push((left, i))
            queue.push((i+1, right))

    return np.asarray(degrees, dtype=np.uint32)
