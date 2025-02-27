from dynamic_array import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initialize a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._heap = DynamicArray()

        # populate MinHeap with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MinHeap content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        heap_data = [self._heap[i] for i in range(self._heap.length())]
        return "HEAP " + str(heap_data)

    def add(self, node: object) -> None:
        """
        Add a new element to the heap

        node (Object): element to be added to the heap
        """
        # Adds the new node to end of the heap
        self._heap.append(node)
        self._percolate_up(self._heap.length() - 1)

    def is_empty(self) -> bool:
        """
        Check if the heap is empty
        """
        # Heap is empty if length = 0
        return self._heap.length() == 0

    def get_min(self) -> object:
        """
        Get the minimum element in the heap

        Raises exception if the heap is empty
        """
        if self.is_empty():
            raise MinHeapException("Heap is empty")
        # Min element will always be index 0
        return self._heap[0]

    def remove_min(self) -> object:
        """
        Removes and returns the minimum element from the heap

        Raises exception if the heap is empty
        """
        if self.is_empty():
            raise MinHeapException("Heap is empty")
        # Stores min val and last val
        min_val = self._heap[0]
        last_val = self._heap[self._heap.length() - 1]
        self._heap[0] = last_val # Move last val to root and removee the last element
        self._heap.remove_at_index(self._heap.length() - 1)
        # Maintains heap property if not empty
        if not self.is_empty():
            self._percolate_down(0)
        
        return min_val

    def build_heap(self, da: DynamicArray) -> None:
        """
        Builds a heap from a dynamic array

        da (DynamicArray): dynamic array used to build heap
        """
        # Build empty dynamic array and copy the elements into the array
        self._heap = DynamicArray()
        for i in range(da.length()):
            self._heap.append(da[i])
        # Percolate down building the heap
        for i in range(self._heap.length() // 2 - 1, -1, -1):
            self._percolate_down(i)

    def size(self) -> int:
        """
        Returns the size of the heap
        """
        return self._heap.length()

    def clear(self) -> None:
        """
        Clears the heap
        """
        self._heap = DynamicArray()

    def _percolate_up(self, index: int) -> None:
        """
        Helper method to maintain the heap property

        index (int): Index to percolate up
        """
        # get parent index
        parent = (index - 1) // 2
        # Percolate up until heap property is restored
        while index > 0 and self._heap[index] < self._heap[parent]:
            self._heap[index], self._heap[parent] = self._heap[parent], self._heap[index]
            index = parent
            parent = (index - 1) // 2

    def _percolate_down(self, index: int) -> None:
        """
        Helper method to maintain the heap property

        index (int): Index to percolate down
        """
        # Get left child index
        child = 2 * index + 1
        # Percolate down until heap property is restored
        while child < self._heap.length():
            min_child = child
            right_child = child + 1
            if right_child < self._heap.length() and self._heap[right_child] < self._heap[child]:
                min_child = right_child
            # Breaks once node is smaller than children and property is restored
            if self._heap[min_child] >= self._heap[index]:
                break

            self._heap[min_child], self._heap[index] = self._heap[index], self._heap[min_child]
            index = min_child
            child = 2 * index + 1

def heapsort(da: DynamicArray) -> None:
    """
    Sort the dynamic array using heapsort algorithm

    da (DynamicArray): Array to be sorted
    """
    heap = MinHeap()
    heap.build_heap(da)
    # Remove the min element from the heap and place it at the end of the array
    for i in range(da.length() - 1, -1, -1):
        da[i] = heap.remove_min()