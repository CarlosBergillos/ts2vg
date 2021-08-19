cdef class PairQueue:
    def __cinit__(self):
        self.queue = <Queue *> malloc(sizeof(Queue))
        self.queue[0].head = NULL
        self.queue[0].tail = NULL
        
    def __dealloc__(self):
        self.free()
        
    cdef void push(self, (unsigned int, unsigned int) values):
        # Create the new entry and fill in the fields in the structure
        cdef QueueEntry *new_entry = <QueueEntry *> malloc(sizeof(QueueEntry))

        if new_entry is NULL:
            raise MemoryError()

        new_entry[0].a = values[0]
        new_entry[0].b = values[1]
        # new_entry[0].prev = self.queue[0].tail
        new_entry[0].next = NULL

        # Insert into the queue tail
        if self.queue[0].tail is NULL:
            # If the queue was previously empty, both the head and
            # tail must be pointed at the new entry
            self.queue[0].head = new_entry
            self.queue[0].tail = new_entry

        else:
            # The current entry at the tail must have next pointed to this
            # new entry
            self.queue[0].tail[0].next = new_entry

            # Only the tail must be pointed at the new entry
            self.queue[0].tail = new_entry
    
    cdef (unsigned int, unsigned int) pop(self):
        cdef QueueEntry *entry
        cdef unsigned int result  # QueueValue result;

        # Check the queue is not empty
        if self.is_empty():
            raise IndexError("Queue is empty")

        # Unlink the first entry from the head of the queue
        entry = self.queue[0].head
        self.queue[0].head = entry[0].next
        a = entry[0].a
        b = entry[0].b

        if self.queue[0].head is NULL:
            # If doing this has unlinked the last entry in the queue, set
            # tail to NULL as well.

            self.queue[0].tail = NULL
        # else:
            # The new first in the queue has no previous entry
            # self.queue[0].head[0].prev = NULL

        # Free back the queue entry structure
        free(entry)

        return a, b

    cdef bint is_empty(self):
        return self.queue[0].head is NULL
    
    def __bool__(self):
        return not self.is_empty()
    
    cdef void free(self):
        # Empty the queue
        while not self.is_empty():
            self.pop()

        # Free back the queue
        free(self.queue)
