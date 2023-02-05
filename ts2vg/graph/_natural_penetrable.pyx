#cython: language_level=3

cimport cython
import numpy as np
cimport numpy as np
from libc.math cimport fabs, INFINITY

from ts2vg.utils.pairqueue cimport PairQueue
from ts2vg.graph.base import _DIRECTED_OPTIONS
from ts2vg.graph._base cimport _greater, _argmax, _argmin, _get_weight_func, weight_func_type

ctypedef unsigned int uint

cdef double ABS_TOL = 1e-14
cdef double REL_TOL = 1e-14
cdef uint _DIRECTED_LEFT_TO_RIGHT = _DIRECTED_OPTIONS['left_to_right']
cdef uint _DIRECTED_TOP_TO_BOTTOM = _DIRECTED_OPTIONS['top_to_bottom']


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _compute_graph(np.float64_t[:] ts, np.float64_t[:] xs, uint directed, uint weighted, bint only_degrees, double min_weight, double max_weight, uint penetrable_limit):
    """
    Computes the limited penetrable visibility graph of a time series.
    """

    # Algorithm implementation comments:
    # Let S be `penetrable_limit + 1`, we use an array of length S (`max_slopes`) to store
    # the S largest slopes seen so far (for each iteration of the outer loop).
    # If a new slope is larger than the current smallest slope in `max_slopes`, then the two nodes have visibility
    # with at most `penetrable_limit` obstructions between them and an edge should be added,
    # and `max_slopes` should be updated to include the new slope and to drop the new smallest slope of `max_slopes`.
    #
    # We assume `penetrable_limit` is very small, so linear search to find the smallest value in `max_slopes`
    # is probably faster than using other advanced data structures like priority queues.

    cdef uint n = ts.size
    cdef list edges = []
    cdef np.uint32_t[:] degrees_in = np.zeros(n, dtype=np.uint32)
    cdef np.uint32_t[:] degrees_out = np.zeros(n, dtype=np.uint32)

    cdef uint left, right, i_a, i_b
    cdef double x_a, x_b, y_a, y_b
    cdef double slope, w
    cdef np.float64_t[:] max_slopes = np.full(penetrable_limit+1, -INFINITY, dtype=np.float64)
    cdef uint threshold_slope_idx = 0
    cdef double threshold_slope = -INFINITY

    cdef weight_func_type weight_func = _get_weight_func(weighted)

    def new_threshold_slope(new_slope):
        # drop the old smallest value in `max_slopes` and replace it with the new slope.
        max_slopes[threshold_slope_idx] = new_slope

        # new threshold slope is the new smallest value in `max_slopes`.
        i_new_min = _argmin(max_slopes, 0, penetrable_limit+1)

        return i_new_min, max_slopes[i_new_min]

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

    for i_a in range(n-1):
        x_a = xs[i_a]
        y_a = ts[i_a]

        # sweep from i towards the right
        threshold_slope = -INFINITY
        max_slopes[:] = -INFINITY
        for i_b in range(i_a+1, n):
            x_b = xs[i_b]
            y_b = ts[i_b]
            slope = (y_b-y_a) / (x_b-x_a)
            tol = max(ABS_TOL, REL_TOL * max(fabs(x_a), fabs(x_b), fabs(y_a), fabs(y_b)))

            if _greater(slope, threshold_slope, tol):
                if directed == _DIRECTED_TOP_TO_BOTTOM and (y_b > y_a):
                    add_edge(i_b, i_a, x_b, x_a, y_b, y_a, slope)
                else:  # left_to_right
                    add_edge(i_a, i_b, x_a, x_b, y_a, y_b, slope)

                threshold_slope_idx, threshold_slope = new_threshold_slope(slope)

    return edges, np.asarray(degrees_in, dtype=np.uint32), np.asarray(degrees_out, dtype=np.uint32)
