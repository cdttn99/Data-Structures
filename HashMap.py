from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the given key and value pair in the hash table

        Key (str): key to update
        """
        # Resize if load factor is greater than 0.5
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)
        # Get initial index
        index = self._hash_function(key) % self._capacity
        i = 0
        # Probe to find correct index
        while True:
            new_index = (index + i * i) % self._capacity
            entry = self._buckets[new_index]
            if entry is None or entry.is_tombstone:
                self._buckets[new_index] = HashEntry(key, value)
                self._size += 1
                return
            elif entry.key == key:
                self._buckets[new_index].value = value
                return
            i += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Resize the hash table to the capacity making sure its a prime number and rehash all existing key value pairs

        new_capacity (int): new capacity of the table
        """
        if new_capacity < 1:
            return

        new_capacity = self._next_prime(new_capacity)
        old_buckets = self._buckets
        self._buckets = DynamicArray()
        self._capacity = new_capacity
        self._size = 0
        # Initialize new buckets
        for _ in range(self._capacity):
            self._buckets.append(None)
        # Rehash all entries
        for index in range(old_buckets.length()):
            entry = old_buckets[index]
            if entry and not entry.is_tombstone:
                self.put(entry.key, entry.value)

    def table_load(self) -> float:
        """
        Returns the load factor of the hash table
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of emty or tombstone buckets in the hash table
        """
        count = 0
        for index in range(self._buckets.length()):
            if self._buckets[index] is None or self._buckets[index].is_tombstone:
                count += 1
        return count
    def get(self, key: str) -> object:
        """
        Gets the value associated with the key from the hash table

        Key (str): key to search for 
        """
        index = self._hash_function(key) % self._capacity
        i = 0
        # Probe to find the key
        while True:
            new_index = (index + i * i) % self._capacity
            entry = self._buckets[new_index]
            if entry is None:
                # Key not found
                return None
            if entry.key == key and not entry.is_tombstone:
                # Key found
                return entry.value
            i += 1

    def contains_key(self, key: str) -> bool:
        """
        Checks if the key exists in the table

        key (str): Key to search for

        Returns true if key exists else false
        """
        return self.get(key) is not None

    def remove(self, key: str) -> None:
        """
        Removes the key value pair aassociated with the key from the hash table

        key (str): key to remove
        """
        index = self._hash_function(key) % self._capacity
        i = 0
        while True:
            new_index = (index + i * i) % self._capacity
            entry = self._buckets[new_index]
            if entry is None:
                return
            if entry.key == key and not entry.is_tombstone:
                # Key is found make it tombstone
                entry.is_tombstone = True
                self._size -= 1
                return
            i += 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Retrieve all nontombstone key value pairs from the hash table as a dynamic array of tuples
        """
        result = DynamicArray()
        for index in range(self._buckets.length()):
            entry = self._buckets[index]
            if entry and not entry.is_tombstone:
                result.append((entry.key, entry.value))
        return result

    def clear(self) -> None:
        """
        Clears all elements from the hash table
        """
        for index in range(self._buckets.length()):
            self._buckets[index] = None
        self._size = 0

    def __iter__(self):
        """
        initializes iterator for hash table
        """
        self._iter_index = 0
        return self

    def __next__(self):
        """
        Returns the next nontombstone entry in the hash table
        """
        while self._iter_index < self._buckets.length():
            entry = self._buckets[self._iter_index]
            self._iter_index += 1
            if entry and not entry.is_tombstone:
                return entry
        raise StopIteration