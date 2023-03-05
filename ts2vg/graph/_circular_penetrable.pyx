#cython: language_level=3
#distutils: language=c++

cimport cython
import numpy as np
cimport numpy as np
from libc.math cimport fabs, INFINITY, NAN, isnan, pi, atan, sin, cos
from libcpp.set cimport multiset as cmultiset
from libcpp.pair cimport pair as cpair

from cython.operator cimport dereference as deref

from ts2vg.graph.base import _DIRECTED_OPTIONS, _WEIGHTED_OPTIONS
from ts2vg.graph._base cimport _greater, _argmax, _argmin, _get_weight_func, weight_func_type

ctypedef unsigned int uint
ctypedef cpair[double, double] double_pair

cdef double ABS_TOL = 1e-14
cdef double REL_TOL = 1e-14
cdef uint _DIRECTED_LEFT_TO_RIGHT = _DIRECTED_OPTIONS['left_to_right']
cdef uint _DIRECTED_TOP_TO_BOTTOM = _DIRECTED_OPTIONS['top_to_bottom']
cdef uint _WEIGHTED_NUM_PENETRATIONS = _WEIGHTED_OPTIONS['num_penetrations']


# cdef cmultiset[double_pair] lines

# lines.insert(double_pair(5, 5))
# lines.insert(double_pair(10, 10))
# lines.insert(double_pair(12, 12))
# lines.insert(double_pair(16, 16))

# print(lines.size())

# cdef cmultiset[double_pair].iterator it = lines.begin()

# while it != lines.upper_bound(double_pair(12, INFINITY)):
#     print(deref(it))
#     inc(it)

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
    cdef uint i_a, i_b
    cdef double x_a, x_b, x_p, y_a, y_b, y_b_line, y_p
    cdef double w
    cdef double_pair line
    cdef double line_slope, line_intercept
    cdef cmultiset[double_pair] lines
    cdef cmultiset[double_pair].iterator lines_it
    cdef double rotation_angle = pi - atan(1 / alpha)

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

        lines.clear()

        for i_b in range(i_a+1, n):
            x_b = xs[i_b]
            y_b = ts[i_b]

            penetrations = 0

            for line in lines:
                line_slope, line_intercept = line.first, line.second
                y_b_line = line_slope * x_b + line_intercept
                
                if y_b_line > y_b:
                    # y_b is obstructed

                    penetrations += 1

                    if penetrations > penetrable_limit:
                        break

            else:
                # TODO: take into account weighted and directed
                add_edge(i_a, i_b, x_a, x_b, y_a, y_b, NAN)
            
                # rotate point (x_a, y_a) around (x_b, y_b) by rotation_angle radians
                x_p = cos(rotation_angle) * (x_a - x_b) - sin(rotation_angle) * (y_a - y_b) + x_b
                y_p = sin(rotation_angle) * (x_a - x_b) + cos(rotation_angle) * (y_a - y_b) + y_b

                # alternatively:
                # slope to angle (atan2)
                # add rotation_angle
                # angle to slope (tan)

                if x_p <= x_b:
                    # line rotated past x_b and is pointing backwards, will not obstruct any upcoming point.
                    continue
                
                # y = m x + n
                # y_b = m x_b + n
                # n = y_b - m x_b
                    
                line_slope = (y_p - y_b) / (x_p - x_b)
                line_intercept = y_b - line_slope * x_b

                if penetrable_limit == 0:
                    # remove previous lines that become redundant. (drop lines that have a smaller slope)
                    # consider std::erase_if if in C++20

                    lines_it = lines.begin()
                    while lines_it != lines.upper_bound(double_pair(line_slope, INFINITY)):
                        lines_it = lines.erase(lines_it)

                lines.insert(double_pair(line_slope, line_intercept))

    #         for i_c in range(i_a+1, i_b):
    #             x_c = xs[i_c]
    #             y_c = ts[i_c]

    #             tol = max(ABS_TOL, REL_TOL * max(fabs(x_a), fabs(x_b), fabs(y_a), fabs(y_b)))

    #             v1_x, v1_y = (x_a - x_c, y_a - y_c)
    #             v2_x, v2_y = (x_b - x_c, y_b - y_c)

    #             angle = _angle_between(v1_x, v1_y, v2_x, v2_y)

    #             if not _greater(angle, threshold_angle, tol):
    #                 penetrations += 1

    #                 if penetrations > penetrable_limit:
    #                     break

    #         else:
    #             if weighted == _WEIGHTED_NUM_PENETRATIONS:
    #                 w = penetrations
    #             else:
    #                 # weight will be computed later by weight_func
    #                 w = NAN

    #             if directed == _DIRECTED_TOP_TO_BOTTOM and (y_b > y_a):
    #                 add_edge(i_b, i_a, x_b, x_a, y_b, y_a, w)
    #             else:  # left_to_right
    #                 add_edge(i_a, i_b, x_a, x_b, y_a, y_b, w)

    return edges, np.asarray(degrees_in, dtype=np.uint32), np.asarray(degrees_out, dtype=np.uint32)
