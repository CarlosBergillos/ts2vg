#cython: language_level=3

cimport cython
import numpy as np
cimport numpy as np
from libc.math cimport INFINITY, NAN

from ts2vg.utils.pairqueue cimport PairQueue
from ts2vg.graph.base import _DIRECTED_OPTIONS
from ts2vg.graph._base cimport _argmax, _argmin, _get_weight_func, weight_func_type

ctypedef unsigned int uint

cdef uint _DIRECTED_LEFT_TO_RIGHT = _DIRECTED_OPTIONS['left_to_right']
cdef uint _DIRECTED_TOP_TO_BOTTOM = _DIRECTED_OPTIONS['top_to_bottom']


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _compute_graph(np.float64_t[:] ts, np.float64_t[:] xs, uint directed, uint weighted, bint only_degrees, double min_weight, double max_weight, uint penetrable_limit):
    """
    Computes the limited penetrable horizontal visibility graph of a time series.
    """

    # Algorithm implementation comments:
    # See comments in _natural_penetrable.pyx.
    # Horizontal case is analogous, replacing slope with height (y),
    # and with the additional benefit than sweeps can be stopped earlier.

    cdef uint n = ts.size
    cdef list edges = []
    cdef np.uint32_t[:] degrees_in = np.zeros(n, dtype=np.uint32)
    cdef np.uint32_t[:] degrees_out = np.zeros(n, dtype=np.uint32)

    cdef uint left, right, i_a, i_b
    cdef double x_a, x_b, y_a, y_b
    cdef double w
    cdef np.float64_t[:] max_ys = np.full(penetrable_limit+1, -INFINITY, dtype=np.float64)
    cdef uint threshold_y_idx = 0
    cdef double threshold_y = -INFINITY

    cdef weight_func_type weight_func = _get_weight_func(weighted)

    def add_edge(uint i1, uint i2, double x1, double x2, double y1, double y2):
        w = weight_func(x1, x2, y1, y2, NAN)

        if w <= min_weight or w >= max_weight:
            return

        degrees_out[i1] += 1
        degrees_in[i2] += 1

        if not only_degrees:
            if weighted > 0:
                edges.append((i1, i2, w))
            else:
                edges.append((i1, i2))

    for i_a in range(n-1):
        x_a = xs[i_a]
        y_a = ts[i_a]

        # sweep from i towards the right
        threshold_y = -INFINITY
        max_ys[:] = -INFINITY
        for i_b in range(i_a+1, n):
            x_b = xs[i_b]
            y_b = ts[i_b]

            if (y_a > threshold_y and y_b > threshold_y):
                if directed == _DIRECTED_TOP_TO_BOTTOM and (y_b > y_a):
                    add_edge(i_b, i_a, x_b, x_a, y_b, y_a)
                else:  # left_to_right
                    add_edge(i_a, i_b, x_a, x_b, y_a, y_b)

                # drop the old smallest value in `max_ys` and replace it with the new y.
                max_ys[threshold_y_idx] = y_b

                # new threshold y is the new smallest value in `max_ys`.
                threshold_y_idx = _argmin(max_ys, 0, penetrable_limit+1)
                threshold_y = max_ys[threshold_y_idx]

                if threshold_y > y_a:
                    # earlier condition will never be satisfied anymore in this sweep
                    break

    return edges, np.asarray(degrees_in, dtype=np.uint32), np.asarray(degrees_out, dtype=np.uint32)
