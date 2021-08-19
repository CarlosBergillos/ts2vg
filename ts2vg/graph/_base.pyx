#cython: language_level=3

cimport cython
cimport numpy as np

from libc.math cimport fabs, atan, sqrt, isnan, NAN

from ts2vg.graph.base import _WEIGHTED_OPTIONS

cdef uint _WEIGHTED_DISTANCE = _WEIGHTED_OPTIONS['distance']
cdef uint _WEIGHTED_SQ_DISTANCE = _WEIGHTED_OPTIONS['sq_distance']
cdef uint _WEIGHTED_V_DISTANCE = _WEIGHTED_OPTIONS['v_distance']
cdef uint _WEIGHTED_ABS_V_DISTANCE = _WEIGHTED_OPTIONS['abs_v_distance']
cdef uint _WEIGHTED_H_DISTANCE = _WEIGHTED_OPTIONS['h_distance']
cdef uint _WEIGHTED_ABS_H_DISTANCE = _WEIGHTED_OPTIONS['abs_h_distance']
cdef uint _WEIGHTED_SLOPE = _WEIGHTED_OPTIONS['slope']
cdef uint _WEIGHTED_ABS_SLOPE = _WEIGHTED_OPTIONS['abs_slope']
cdef uint _WEIGHTED_ANGLE = _WEIGHTED_OPTIONS['angle']
cdef uint _WEIGHTED_ABS_ANGLE = _WEIGHTED_OPTIONS['abs_angle']

@cython.boundscheck(False)
@cython.wraparound(False)
cdef uint _argmax(np.float64_t[:] a, uint left, uint right):
    """Get the argmax of 'a', between indexes 'left' and 'right'."""
    cdef uint i
    cdef uint idx = left
    cdef double val = a[left]

    for i in range(left+1, right):
        if a[i] > val:
            val = a[i]
            idx = i
    return idx


@cython.cdivision(True)
cdef inline double _get_weight(uint weighted, double x_a, double x_b, double y_a, double y_b, double slope):
    if weighted == _WEIGHTED_DISTANCE:
        return sqrt(((x_b - x_a) * (x_b - x_a)) + ((y_b - y_a) * (y_b - y_a)))
    
    elif weighted == _WEIGHTED_SQ_DISTANCE:
        return ((x_b - x_a) * (x_b - x_a)) + ((y_b - y_a) * (y_b - y_a))
    
    elif weighted == _WEIGHTED_V_DISTANCE:
        return y_b - y_a

    elif weighted == _WEIGHTED_ABS_V_DISTANCE:
        return fabs(y_b - y_a)

    elif weighted == _WEIGHTED_H_DISTANCE:
        return x_b - x_a

    elif weighted == _WEIGHTED_ABS_H_DISTANCE:
        return fabs(x_b - x_a)

    elif weighted == _WEIGHTED_SLOPE:
        if isnan(slope):
            slope = (y_b-y_a) / (x_b-x_a)
        return slope

    elif weighted == _WEIGHTED_ABS_SLOPE:
        if isnan(slope):
            slope = (y_b-y_a) / (x_b-x_a)
        return fabs(slope)

    elif weighted == _WEIGHTED_ANGLE:
        if isnan(slope):
            slope = (y_b-y_a) / (x_b-x_a)
        return atan(slope)

    elif weighted == _WEIGHTED_ABS_ANGLE:
        if isnan(slope):
            slope = (y_b-y_a) / (x_b-x_a)
        return atan(fabs(slope))

    return NAN


cdef inline tuple _edge_tuple(uint i_a, uint i_b, double x_a, double x_b, double y_a, double y_b, double slope, uint weighted):
    if weighted > 0:
        w = _get_weight(weighted, x_a, x_b, y_a, y_b, slope)
        return (i_a, i_b, w)
    else:
        return (i_a, i_b)
