class SparseMatrix:
    def __init__(self, nrows, ncols, default_value):
        self._nrows = nrows
        self._ncols = ncols
        self._default_value = default_value
        self.sparse_list = None
        self.clear()

    def clear(self):
        # this method to clear out row to default value while keeping row _size
        self.sparse_list = [OrderedLinkedList() for _ in range(self._nrows)]

    def get(self, row, col):
        self._validate_row_col(row, col)
        try:
            data = self.sparse_list[row].search(col)
            return data.value
        except AttributeError:
            # if there is no col, return default
            return self._default_value

    def set(self, row, col, val):
        self._validate_row_col(row, col)
        list_row = self.sparse_list[row]
        # if val == self._default, remove from LL
        if val == self._default_value:
            list_row.remove(col)
            return
        # if OLL is empty, add head since insert_at adds to head if empty
        if list_row.is_empty():
            list_row.add(MatrixEntry(0, self._default_value))

        matrix_entry = list_row.search(col)
        if matrix_entry is not None:
            # update if entry exists
            matrix_entry.value = val
        else:
            list_row.insert_at(col, MatrixEntry(col, val))

    def show_sub_square(self, start, size):
        """ start == (start, start) as anchor
            size == (size, size) of the return sub_square
            end == start + size
        """
        end = start + size
        ret_str = ''
        for row in range(start, end):
            for col in range(start, end):
                ret = f'{self.get(row, col) :.2f}  '
                ret_str += f'{ret: >8}'
            ret_str += '\n'
        print(ret_str)
        return ret_str

    def _validate_row_col(self, row, col):
        if row < 0 or row >= self._nrows:
            raise self.OutOfBounds(f"{row} is out of bounds 0 - {self._nrows}", row)
        if col < 0 or col >= self._ncols:
            raise self.OutOfBounds(f"{col} is out of bounds 0 - {self._ncols}", col)

    class OutOfBounds(Exception):
        def __init__(self, message, errors):
            super().__init__(message)
            self.errors = errors


MAT_SIZE = 800

def main():

    mat = SparseMatrix(MAT_SIZE, MAT_SIZE, 0)
    # test mutators
    mat.set(2, 5, 10)
    mat.set(2, 5, 35)  # should overwrite the 10
    mat.set(3, 9, 21)
    try:
        mat.set(MAT_SIZE, 1, 5)  # should fail silently
        print("oops")
    except SparseMatrix.OutOfBounds:
        print("Out of Bounds caught")

    mat.set(9, 9, mat.get(3, 9))  # should copy the 21 here
    mat.set(4, 4, -9)
    mat.set(4, 4, 0)  # should remove the -9 node entirely
    mat.set(MAT_SIZE-1, MAT_SIZE-1, 99)

    # test accessors and exceptions
    try:
        print(mat.get(7, 8))
        print(mat.get(2, 5))
        print(mat.get(9, 9))
        print(mat.get(-4, 7))  # should throw an exception
    except SparseMatrix.OutOfBounds:
        print("Ooops!")

        # show top left 15 x15
        mat.show_sub_square(0, 15)

        # show bottom right 15 x15
        mat.show_sub_square(MAT_SIZE - 15, 15)



# def main():
#     MAT_SIZE = 800
#     mat = SparseMatrix(MAT_SIZE, MAT_SIZE, 0)
#     # test mutators
#     mat.set(2, 5, 10)
#     mat.set(2, 5, 35)  # should overwrite the 10
#     mat.set(3, 5, 10)
#     mat.set(3, 5, 0)
#     mat.set(4, 6, 0)
#     mat.set(1, 0, 40)
#
#     print(type(mat.sparse_list[3].search(9)))
#
#     try:
#         mat.set(MAT_SIZE, 1, 5)  # should fail silently
#         print("oops")
#     except SparseMatrix.OutOfBounds:
#         print("Out of Bounds caught")
#
#     mat.set(9, 9, mat.get(3, 9))  # should copy the 21 here
#     mat.set(4, 4, -9)
#     mat.set(4, 4, 0)  # should remove the -9 node entirely
#     mat.set(MAT_SIZE-1, MAT_SIZE-1, 99)
#
#      # test accessors and exceptions
#     try:
#         print(mat.get(7, 8))
#         print(mat.get(2, 5))
#         print(mat.get(9, 9))
#         print(mat.get(-4, 7))  # should throw an exception
#     except SparseMatrix.OutOfBounds:
#         print("Ooops!")
#
#     # show top left 15 x15
#     mat.show_sub_square(0, 15)
#
#     # show bottom right 15 x15
#     mat.show_sub_square(MAT_SIZE - 15, 15)




class MatrixEntry:
    def __init__(self, column, value):
        self._column = column
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __eq__(self, other):
        if isinstance(other, MatrixEntry):
            return self._column == other._column
        else:
            return self._column == other

    def __lt__(self, other):
        if isinstance(other, MatrixEntry):
            return self._column < other._column
        else:
            return self._column < other

    def __gt__(self, other):
        return not self.__lt__(other) and not self.__eq__(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __le__(self, other):
        return not self.__gt__(other)

class OrderedLinkedList:
    def __init__(self):
        self._head = None
        self._search_pred = None

    def add(self, data):
        new_node = LinkedListNode(data)
        new_node.next = self._head
        self._head = new_node

    def is_empty(self):
        return self._head is None

    def search(self, data):
        current = self._head
        self._search_pred = None
        while current is not None:
            if current.data == data:
                return current.data
            self._search_pred = current
            current = current.next
        return None

    def remove(self, data):
        if self.search(data) is None:
            return False
        else:
            if self._search_pred is None:
                # data found at head
                self._head = self._head.next
            else:
                item_to_delete = self._search_pred.next
                self._search_pred.next = item_to_delete.next
            return True

    def insert_at(self, item, data):
        if self.is_empty() or item == 0:
            self.add(data)
            return True
        new_node = LinkedListNode(data)
        current = self._head
        for i in range(item - 1):
            if current.next is None:
                current.next = new_node
                return True
            current = current.next
        new_node.next = current.next
        current.next = new_node
        return True

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise ValueError
        else:
            if self.is_empty():
                raise IndexError
            current = self._head
            for i in range(item):
                current = current.next
                if current is None:
                    raise IndexError
            return current.data

    def __iter__(self):
        current = self._head
        while current is not None:
            yield current.data
            current = current.next

class LinkedListNode:
    def __init__(self, init_data):
        self._data = init_data
        self._next = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = new_data

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, new_next):
        self._next = new_next


if __name__ == "__main__":
    main()
