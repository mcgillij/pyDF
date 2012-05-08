import heapq

class PriorityQueueSet(object):
    """ Combined priority queue and set data structure. Acts like
        a priority queue, except that its items are guaranteed to
        be unique.
        
        Provides O(1) membership test and O(log N) removal of the 
        *smallest* item. Addition is more complex. When the item 
        doesn't exist, it's added in O(log N). When it already 
        exists, its priority is checked against the new item's
        priority in O(1). If the new item's priority is smaller,
        it is updated in the queue. This takes O(N).
        
        Important: The items you store in the queue have identity
        (that determines when two items are the same, as far as
        you're concerned) and priority. Therefore, you must 
        implement the following operators for them: __hash__, 
        __cmp__ and __eq__.
        
        *   __eq__ will be used for exact comparison of items. It 
            must return True if and only if the items are identical
            from your point of view (although their priorities can
            be different)
        *   __cmp__ will be used to compare priorities. Two items
            can be different and have the same priority, and even
            be equal but have different priorities (though they
            can't be in the queue at the same time)
        *   __hash__ will be used to hash the items for 
            efficiency. To implement it, you almost always have 
            to just call hash() on the attribute you're comparing
            in __eq__
            
        Note that for native Python objects (strings, tuples, 
        etc.) these operators are already defined as needed.
    """
    def __init__(self):
        """ Create a new PriorityQueueSet
        """
        self.set = {}
        self.heap = []    

    def __len__(self):
        return len(self.heap)

    def has_item(self, item):
        """ Check if *item* exists in the queue
        """
        return item in self.set
    
    def pop_smallest(self):
        """ Remove and return the smallest item from the queue.
            IndexError will be thrown if the queue is empty.
        """
        smallest = heapq.heappop(self.heap)
        del self.set[smallest]
        return smallest
    
    def add(self, item):
        """ Add *item* to the queue. 
        
            If such an item already exists, its priority will be 
            checked versus *item*. If *item*'s priority is better
            (i.e. lower), the priority of the existing item in the 
            queue will be updated.
        
            Returns True iff the item was added or updated.
        """
        if not item in self.set:
            self.set[item] = item
            heapq.heappush(self.heap, item)
            return True
        elif item < self.set[item]:
            # No choice but to search linearly in the heap
            for idx, old_item in enumerate(self.heap):
                if old_item == item:
                    del self.heap[idx]
                    self.heap.append(item)
                    heapq.heapify(self.heap)
                    self.set[item] = item
                    return True
        
        return False
        
