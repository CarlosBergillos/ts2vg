#cython: language_level=3

cimport cython
cimport numpy as np

from libc.math cimport fabs, atan, sqrt, isnan, NAN

from ts2vg.graph.base import _WEIGHTED_OPTIONS

cdef uint _UNWEIGHTED = _WEIGHTED_OPTIONS[None]
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


cdef inline bint _greater(double a, double b, double tolerance):
    return (a - b) > tolerance


@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline uint _argmax(np.float64_t[:] a, uint left, uint right):
    """Get the argmax of 'a', between indexes 'left' and 'right'."""
    cdef uint i
    cdef uint idx = left
    cdef double val = a[left]

    for i in range(left+1, right):
        if a[i] > val:
            val = a[i]
            idx = i
    return idx


@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline uint _argmin(np.float64_t[:] a, uint left, uint right):
    """Get the argmin of 'a', between indexes 'left' and 'right'."""
    cdef uint i
    cdef uint idx = left
    cdef double val = a[left]

    for i in range(left+1, right):
        if a[i] < val:
            val = a[i]
            idx = i
    return idx



cdef inline double _weight_0(double x_a, double x_b, double y_a, double y_b, double slope):
    return 0


cdef inline double _weight_nan(double x_a, double x_b, double y_a, double y_b, double slope):
    return NAN


cdef inline double _weight_distance(double x_a, double x_b, double y_a, double y_b, double slope):
    return sqrt(((x_b - x_a) * (x_b - x_a)) + ((y_b - y_a) * (y_b - y_a)))


cdef inline double _weight_sq_distance(double x_a, double x_b, double y_a, double y_b, double slope):
    return ((x_b - x_a) * (x_b - x_a)) + ((y_b - y_a) * (y_b - y_a))


cdef inline double _weight_v_distance(double x_a, double x_b, double y_a, double y_b, double slope):
    return y_b - y_a


cdef inline double _weight_abs_v_distance(double x_a, double x_b, double y_a, double y_b, double slope):
    return fabs(y_b - y_a)


cdef inline double _weight_h_distance(double x_a, double x_b, double y_a, double y_b, double slope):
    return x_b - x_a


cdef inline double _weight_abs_h_distance(double x_a, double x_b, double y_a, double y_b, double slope):
    return fabs(x_b - x_a)


@cython.cdivision(True)
cdef inline double _weight_slope(double x_a, double x_b, double y_a, double y_b, double slope):
    if isnan(slope):
        slope = (y_b-y_a) / (x_b-x_a)
    return slope


@cython.cdivision(True)
cdef inline double _weight_abs_slope(double x_a, double x_b, double y_a, double y_b, double slope):
    if isnan(slope):
        slope = (y_b-y_a) / (x_b-x_a)
    return fabs(slope)


@cython.cdivision(True)
cdef inline double _weight_angle(double x_a, double x_b, double y_a, double y_b, double slope):
    if isnan(slope):
        slope = (y_b-y_a) / (x_b-x_a)
    return atan(slope)


@cython.cdivision(True)
cdef inline double _weight_abs_angle(double x_a, double x_b, double y_a, double y_b, double slope):
    if isnan(slope):
        slope = (y_b-y_a) / (x_b-x_a)
    return atan(fabs(slope))


cdef weight_func_type _get_weight_func(uint weighted):
    if weighted == _UNWEIGHTED:
        return _weight_0

    if weighted == _WEIGHTED_DISTANCE:
        return _weight_distance
    
    elif weighted == _WEIGHTED_SQ_DISTANCE:
        return _weight_sq_distance
    
    elif weighted == _WEIGHTED_V_DISTANCE:
        return _weight_v_distance

    elif weighted == _WEIGHTED_ABS_V_DISTANCE:
        return _weight_abs_v_distance
    
    elif weighted == _WEIGHTED_H_DISTANCE:
        return _weight_h_distance

    elif weighted == _WEIGHTED_ABS_H_DISTANCE:
        return _weight_abs_h_distance
    
    elif weighted == _WEIGHTED_SLOPE:
        return _weight_slope

    elif weighted == _WEIGHTED_ABS_SLOPE:
        return _weight_abs_slope
    
    elif weighted == _WEIGHTED_ANGLE:
        return _weight_angle

    elif weighted == _WEIGHTED_ABS_ANGLE:
        return _weight_abs_angle

    else:
        return _weight_nan
