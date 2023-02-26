#cython: language_level=3

cimport cython
import numpy as np
cimport numpy as np
from libc.math cimport fabs, INFINITY, NAN, isnan, pi, atan, atan2

from ts2vg.graph.base import _DIRECTED_OPTIONS, _WEIGHTED_OPTIONS
from ts2vg.graph._base cimport _greater, _argmax, _argmin, _get_weight_func, weight_func_type

ctypedef unsigned int uint

cdef double ABS_TOL = 1e-14
cdef double REL_TOL = 1e-14
cdef uint _DIRECTED_LEFT_TO_RIGHT = _DIRECTED_OPTIONS['left_to_right']
cdef uint _DIRECTED_TOP_TO_BOTTOM = _DIRECTED_OPTIONS['top_to_bottom']
cdef uint _WEIGHTED_NUM_PENETRATIONS = _WEIGHTED_OPTIONS['num_penetrations']


cdef double _angle_between(double v1_x, double v1_y, double v2_x, double v2_y):
    """Returns the angle in radians between vectors 'v1' and 'v2'."""
    cdef double angle1, angle2, angle_diff

    angle1 = atan2(v1_y, v1_x)
    angle2 = atan2(v2_y, v2_x)

    angle_diff = angle2 - angle1

    if angle_diff < 0:
        angle_diff += 2 * pi

    return angle_diff


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def _compute_graph(np.float64_t[:] ts, np.float64_t[:] xs, double alpha, uint directed, uint weighted, bint only_degrees, double min_weight, double max_weight, uint penetrable_limit):
    """
    Computes the limited penetrable circular visibility graph of a time series.
    """

    cdef uint n = ts.size
    cdef list edges = []
    cdef np.uint32_t[:] degrees_in = np.zeros(n, dtype=np.uint32)
    cdef np.uint32_t[:] degrees_out = np.zeros(n, dtype=np.uint32)

    cdef uint penetrations
    cdef uint i_a, i_b, i_c
    cdef double x_a, x_b, x_c, y_a, y_b, y_c
    cdef double w, v1_x, v1_y, v2_x, v2_y
    cdef double angle
    cdef double threshold_angle = pi - atan(1 / alpha)

    cdef weight_func_type weight_func = _get_weight_func(weighted)

    def add_edge(uint i1, uint i2, double x1, double x2, double y1, double y2, double known_w):
        if isnan(known_w):
            w = weight_func(x1, x2, y1, y2, NAN)
        else:
            w = known_w

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

        for i_b in range(i_a+1, n):
            x_b = xs[i_b]
            y_b = ts[i_b]

            penetrations = 0

            for i_c in range(i_a+1, i_b):
                x_c = xs[i_c]
                y_c = ts[i_c]

                tol = max(ABS_TOL, REL_TOL * max(fabs(x_a), fabs(x_b), fabs(y_a), fabs(y_b)))

                v1_x, v1_y = (x_a - x_c, y_a - y_c)
                v2_x, v2_y = (x_b - x_c, y_b - y_c)

                angle = _angle_between(v1_x, v1_y, v2_x, v2_y)

                if not _greater(angle, threshold_angle, tol):
                    penetrations += 1

                    if penetrations > penetrable_limit:
                        break

            else:
                if weighted == _WEIGHTED_NUM_PENETRATIONS:
                    w = penetrations
                else:
                    # weight will be computed later by weight_func
                    w = NAN

                if directed == _DIRECTED_TOP_TO_BOTTOM and (y_b > y_a):
                    add_edge(i_b, i_a, x_b, x_a, y_b, y_a, w)
                else:  # left_to_right
                    add_edge(i_a, i_b, x_a, x_b, y_a, y_b, w)

    return edges, np.asarray(degrees_in, dtype=np.uint32), np.asarray(degrees_out, dtype=np.uint32)
