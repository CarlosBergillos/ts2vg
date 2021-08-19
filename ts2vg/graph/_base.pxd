#cython: language_level=3

cimport numpy as np

ctypedef unsigned int uint

cdef uint _argmax(np.float64_t[:] a, uint left, uint right)

cdef double _get_weight(uint weighted, double x_a, double x_b, double y_a, double y_b, double slope)

cdef tuple _edge_tuple(uint i_a, uint i_b, double x_a, double x_b, double y_a, double y_b, double slope, uint weighted)