#cython: language_level=3

cimport numpy as np

ctypedef unsigned int uint
ctypedef double (*weight_func_type)(double x_a, double x_b, double y_a, double y_b, double slope)

cdef uint _argmax(np.float64_t[:] a, uint left, uint right)

cdef weight_func_type _get_weight_func(uint weighted)

cdef tuple _edge_tuple(uint i_a, uint i_b, double x_a, double x_b, double y_a, double y_b, double slope, weight_func_type weight_func)