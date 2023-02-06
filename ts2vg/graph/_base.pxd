#cython: language_level=3

cimport numpy as np

ctypedef unsigned int uint
ctypedef double (*weight_func_type)(double x_a, double x_b, double y_a, double y_b, double slope)

cdef bint _greater(double a, double b, double tolerance)

cdef uint _argmax(np.float64_t[:] a, uint left, uint right)

cdef uint _argmin(np.float64_t[:] a, uint left, uint right)

cdef weight_func_type _get_weight_func(uint weighted)
