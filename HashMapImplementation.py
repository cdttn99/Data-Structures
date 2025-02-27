from static_array import StaticArray


class DynamicArrayException(Exception):

    pass


class DynamicArray:
    def __init__(self, start_array=None):
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)

        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        out = "DYN_ARR Size/Cap: "
        out += str(self._size) + "/" + str(self._capacity) + ' ['
        out += ', '.join([str(self._data[_]) for _ in range(self._size)])
        return out + ']'

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        try:
            value = self[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value

    def get_at_index(self, index: int) -> object:
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        self._data[index] = value

    def __getitem__(self, index) -> object:
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        return self._size == 0

    def length(self) -> int:
        return self._size

    def get_capacity(self) -> int:
        return self._capacity

    def print_da_variables(self) -> None:
        print(f"Length: {self._size}, Capacity: {self._capacity}, {self._data}")

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        if new_capacity <= 0 or new_capacity < self._size:
            return  # No work to be done, exit immediately
        # Creates a temp arr with new_capacity, and uses the same data
        new_data = StaticArray(new_capacity)
        for i in range(self._size):
            new_data.set(i, self._data.get(i))
        # Moves temp arr into the StaticArray
        self._data = new_data
        self._capacity = new_capacity

    def append(self, value: object) -> None:
       # Checks for needed size increase and increases to 2x
        if self._size == self._capacity:
            new_capacity = self._capacity * 2
            new_data = StaticArray(new_capacity)
            for i in range(self._size):
                new_data.set(i, self._data.get(i))
            # Copies elements from new_data to old Array
            self._data = new_data
            self._capacity = new_capacity
        self._data.set(self._size, value)
        self._size += 1

    def insert_at_index(self, index: int, value: object) -> None:
        # Checks for Invalid indexs 
        if index < 0 or index > self._size:
            raise DynamicArrayException("Invalid index")
        # Checks for needed size increase
        if self._size == self._capacity:
            new_capacity = self._capacity * 2
            self.resize(new_capacity)

        # Shift elements to the right to make space for the new value
        for i in range(self._size, index, -1):
            self._data.set(i, self._data.get(i - 1))

        # Insert the new value at the specified index
        self._data.set(index, value)
        self._size += 1

    def remove_at_index(self, index: int) -> None:
        # Checks for Invalid Indexs
        if index < 0 or index >= self._size:
            raise DynamicArrayException("Invalid index")

        # Check if size reduction is needed before removal
        if self._capacity > 10 and self._size < self._capacity / 4:
            new_capacity = max(self._size * 2, 10)
            self.resize(new_capacity)

        # Shift elements to the left to overwrite the removed element
        for i in range(index, self._size - 1):
            self._data.set(i, self._data.get(i + 1))

        # Decrease size
        self._size -= 1

    def slice(self, start_index: int, size: int) -> "DynamicArray":
        # Checks for Invalid Index or Size
        if start_index < 0 or start_index >= self._size or size < 0:
            raise DynamicArrayException("Invalid start index or size")
        # Verifies Array has enough Elements
        if start_index + size > self._size:
            raise DynamicArrayException("Not enough elements to make the slice")
        # Creates dynamic array for storage
        sliced_array = DynamicArray()
        for i in range(start_index, start_index + size):
            sliced_array.append(self._data.get(i))
    
        return sliced_array

    def map(self, map_func) -> "DynamicArray":
        # Creates new dynamic array to iterate over the original arrays elements
        mapped_array = DynamicArray()
        for i in range(self._size):
            # Applies Map function and appends to the Array
            mapped_value = map_func(self._data.get(i))
            mapped_array.append(mapped_value)
    
        return mapped_array

    def filter(self, filter_func) -> "DynamicArray":
        # Creates new dynamic array to iterate over the original array elements
        filtered_array = DynamicArray()
        for i in range(self._size):
            # Applys the filter and returns function with only true elements
            if filter_func(self._data.get(i)):
                filtered_array.append(self._data.get(i))
    
        return filtered_array

    def reduce(self, reduce_func, initializer=None) -> object:
       
        if self._size == 0:
            return initializer

        if initializer is None:
            result = self._data.get(0)
            start_index = 1
        else:
            result = initializer
            start_index = 0

        for i in range(start_index, self._size):
            result = reduce_func(result, self._data.get(i))

        return result


def chunk(arr: DynamicArray) -> "DynamicArray":
    if arr.is_empty():
        return DynamicArray()
    
    chunks = DynamicArray()
    current_chunk = DynamicArray()

    # Iterate through the input array
    for i in range(arr.length()):
        # If current_chunk is empty or the current value is greater than or equal to the last value in current_chunk append the value to current_chunk
        if current_chunk.is_empty() or arr.get_at_index(i) >= current_chunk[current_chunk.length() - 1]:
            current_chunk.append(arr.get_at_index(i))
        else:
            # If the current value is less than the last value in current_chunk, append current_chunk to chunks
            chunks.append(current_chunk)
            # Start a new current_chunk with the current value
            current_chunk = DynamicArray()
            current_chunk.append(arr.get_at_index(i))

    # Append the last current_chunk to chunks
    chunks.append(current_chunk)

    return chunks


def find_mode(arr: DynamicArray) -> tuple[DynamicArray, int]:
    
    mode_values = DynamicArray()  
    max_frequency = 0  
    current_frequency = 1  
    current_value = arr.get_at_index(0)  
    mode_values.append(current_value)  
    
    # Iterate through the array starting from the second element
    for i in range(1, arr.length()):
        next_value = arr.get_at_index(i)
        
        # If the current element is the same as the next one
        if next_value == current_value:
            current_frequency += 1
        else:
            if current_frequency > max_frequency:
                # Update max frequency and clear mode_values to store the new mode(s)
                max_frequency = current_frequency
                mode_values = DynamicArray()  # Create a new empty array
                mode_values.append(current_value)
            elif current_frequency == max_frequency:
                mode_values.append(current_value)
            
            # Update current element and reset frequency count for the new element
            current_value = next_value
            current_frequency = 1
    
    # Check frequency of the last element
    if current_frequency > max_frequency:
        max_frequency = current_frequency
        mode_values = DynamicArray()
        mode_values.append(current_value)
    elif current_frequency == max_frequency:
        mode_values.append(current_value)
    
    return mode_values, max_frequency
