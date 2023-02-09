#cython: language_level=3

from libc.stdlib cimport malloc, free

cdef struct QueueEntry:
    unsigned int a;
    unsigned int b;
    # QueueEntry *prev;
    QueueEntry *next;

cdef struct Queue:
    QueueEntry *head;
    QueueEntry *tail;
    
cdef class PairQueue:
    cdef Queue *queue
    
    cdef void push(self, (unsigned int, unsigned int) values)
    cdef (unsigned int, unsigned int) pop(self)
    cdef bint is_empty(self)
    cdef void free(self)
