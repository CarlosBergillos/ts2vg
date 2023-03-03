#cython: language_level=3
#distutils: language=c++

cimport cython
import numpy as np
cimport numpy as np
from libc.math cimport fabs, INFINITY
from libcpp.queue cimport queue as cqueue
from libcpp.pair cimport pair as cpair

from ts2vg.graph.base import _DIRECTED_OPTIONS
from ts2vg.graph._base cimport _greater, _argmax, _get_weight_func, weight_func_type

ctypedef unsigned int uint
ctypedef cpair[uint, uint] uint_pair

cdef double ABS_TOL = 1e-14
cdef double REL_TOL = 1e-14
cdef uint _DIRECTED_LEFT_TO_RIGHT = _DIRECTED_OPTIONS['left_to_right']
cdef uint _DIRECTED_TOP_TO_BOTTOM = _DIRECTED_OPTIONS['top_to_bottom']


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _compute_graph(np.float64_t[:] ts, np.float64_t[:] xs, uint directed, uint weighted, bint only_degrees, double min_weight, double max_weight):
    """
    Computes the visibility graph of a time series
    using a divide-and-conquer strategy.
    """
    cdef uint n = ts.size
    cdef list edges = []
    cdef np.uint32_t[:] degrees_in = np.zeros(n, dtype=np.uint32)
    cdef np.uint32_t[:] degrees_out = np.zeros(n, dtype=np.uint32)

    cdef uint left, right, i, d
    cdef double x_a, x_b, y_a, y_b
    cdef double slope, max_slope, w

    cdef weight_func_type weight_func = _get_weight_func(weighted)

    cdef cqueue[uint_pair] queue
    queue.push(uint_pair(0, n))

    def add_edge(uint i1, uint i2, double x1, double x2, double y1, double y2, double slope):
        w = weight_func(x1, x2, y1, y2, slope)

        if w <= min_weight or w >= max_weight:
            return

        degrees_out[i1] += 1
        degrees_in[i2] += 1

        if not only_degrees:
            if weighted > 0:
                edges.append((i1, i2, w))
            else:
                edges.append((i1, i2))


    while not queue.empty():
        pair = queue.front()
        left, right = pair.first, pair.second
        queue.pop()

        if left+1 < right:
            i = _argmax(ts, left, right)
            x_a = xs[i]
            y_a = ts[i]

            # sweep from i towards the left
            max_slope = -INFINITY
            for d in range(1, i-left+1):
                x_b = xs[i-d]
                y_b = ts[i-d]
                slope = (y_b-y_a) / -(x_b-x_a)  # note: x-axis reversed because sweeping from left to right
                tol = max(ABS_TOL, REL_TOL * max(fabs(x_a), fabs(x_b), fabs(y_a), fabs(y_b)))

                if _greater(slope, max_slope, tol):
                    if directed == _DIRECTED_TOP_TO_BOTTOM:
                        add_edge(i, i-d, x_a, x_b, y_a, y_b, -slope)
                    else:  # left_to_right
                        add_edge(i-d, i, x_b, x_a, y_b, y_a, -slope)
                    
                    max_slope = slope
                    

            # sweep from i towards the right
            max_slope = -INFINITY
            for d in range(1, right-i):
                x_b = xs[i+d]
                y_b = ts[i+d]
                slope = (y_b-y_a) / (x_b-x_a)
                tol = max(ABS_TOL, REL_TOL * max(fabs(x_a), fabs(x_b), fabs(y_a), fabs(y_b)))

                if _greater(slope, max_slope, tol):
                    # note, single case works for both top_to_bottom and left_to_right orders
                    add_edge(i, i+d, x_a, x_b, y_a, y_b, slope)

                    max_slope = slope

            queue.push(uint_pair(left, i))
            queue.push(uint_pair(i+1, right))

    return edges, np.asarray(degrees_in, dtype=np.uint32), np.asarray(degrees_out, dtype=np.uint32)
