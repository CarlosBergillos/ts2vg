#cython: language_level=3

cimport cython
import numpy as np
cimport numpy as np
from libc.math cimport INFINITY

from ts2vg.utils.pairqueue cimport PairQueue
from ts2vg.graph.base import _DIRECTED_OPTIONS
from ts2vg.graph._base cimport _argmax, _edge_tuple

ctypedef unsigned int uint

cdef uint _DIRECTED_LEFT_TO_RIGHT = _DIRECTED_OPTIONS['left_to_right']
cdef uint _DIRECTED_TOP_TO_BOTTOM = _DIRECTED_OPTIONS['top_to_bottom']


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _compute_graph(np.float64_t[:] ts, np.float64_t[:] xs, uint directed, uint weighted, bint only_degrees):
    """
    Computes the visibility graph of a time series
    using a divide-and-conquer strategy.
    """
    cdef uint n = ts.size
    edges = []
    cdef np.uint32_t[:] degrees_in = np.zeros(n, dtype=np.uint32)
    cdef np.uint32_t[:] degrees_out = np.zeros(n, dtype=np.uint32)

    cdef uint left, right, i, d
    cdef double x_a, x_b, y_a, y_b
    cdef double slope, max_slope

    cdef PairQueue queue = PairQueue()
    queue.push((0, n))

    while not queue.is_empty():
        (left, right) = queue.pop()

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

                if slope > max_slope:
                    if directed == _DIRECTED_TOP_TO_BOTTOM:
                        degrees_out[i] += 1
                        degrees_in[i-d] += 1

                        if not only_degrees:
                            edges.append(_edge_tuple(i, i-d, x_a, x_b, y_a, y_b, -slope, weighted))

                    else:  # left_to_right
                        degrees_out[i-d] += 1
                        degrees_in[i] += 1

                        if not only_degrees:
                            edges.append(_edge_tuple(i-d, i, x_b, x_a, y_b, y_a, -slope, weighted))

                    max_slope = slope

            # sweep from i towards the right
            max_slope = -INFINITY
            for d in range(1, right-i):
                x_b = xs[i+d]
                y_b = ts[i+d]
                slope = (y_b-y_a) / (x_b-x_a)

                if slope > max_slope:
                    # note, single case works for both top_to_bottom and left_to_right orders
                    degrees_out[i] += 1
                    degrees_in[i+d] += 1

                    if not only_degrees:
                        edges.append(_edge_tuple(i, i+d, x_a, x_b, y_a, y_b, slope, weighted))

                    max_slope = slope

            queue.push((left, i))
            queue.push((i+1, right))

    return edges, np.asarray(degrees_in, dtype=np.uint32), np.asarray(degrees_out, dtype=np.uint32)
