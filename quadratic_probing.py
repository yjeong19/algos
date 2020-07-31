from ebook import *
import math
import copy
import random
from BinarySearchTree import BinarySearchTree
from AVLTree import AVLTree
import time

class HashEntry:

    class State(Enum):
        ACTIVE = 0
        EMPTY = 1
        DELETED = 2

    def __init__(self, data=None):
        self._data = data
        self._state = HashEntry.State.EMPTY

class HashQP:

    class NotFoundError(Exception):
        pass

    INIT_TABLE_SIZE = 97
    INIT_MAX_LAMBDA = .49

    def __init__(self, table_size=None):
        if table_size is None or table_size < HashQP.INIT_TABLE_SIZE:
            self._table_size = self._next_prime(HashQP.INIT_TABLE_SIZE)
        else:
            self._table_size = self._next_prime(table_size)

        self._buckets = [HashEntry() for _ in range(self._table_size)]
        self._max_lambda = HashQP.INIT_MAX_LAMBDA
        self._size = 0
        self._load_size = 0

    def _internal_hash(self, item):
        return hash(item) % self._table_size

    def _next_prime(self, floor):
        # loop doesnt work for 2 or 3
        if floor <= 2:
            return 2
        elif floor == 3:
            return 3

        if floor % 2 == 0:
            candidate = floor + 1
        else:
            candidate = floor

        while True:
            # we know candidate is odd, check for divisibility by 3
            if candidate % 3 != 0:
                loop_lim = int((math.sqrt(candidate) + 1)/6)

                # now check for divi by 6k +- 1 up to sqrt
                for k in range(1, loop_lim + 1):
                    if candidate % (6 * k - 1) == 0:
                        break
                    if candidate % (6 * k + 1) == 0:
                        break
                    if k == loop_lim:
                        return candidate

            candidate += 2

    def _find_pos(self, data):
        # returns the first location in our probe sequence that is either empty or contains the target data
        kth_odd_number = 1
        bucket = self._internal_hash(data)
        while self._buckets[bucket]._state != HashEntry.State.EMPTY and self._buckets[bucket]._data != data:
            bucket += kth_odd_number
            kth_odd_number += 2
            if bucket >= self._table_size:
                bucket -= self._table_size

        return bucket

    def __contains__(self, item):
        bucket = self._find_pos(item)
        return self._buckets[bucket]._state == HashEntry.State.ACTIVE

    def remove(self, data):
        bucket = self._find_pos(data)
        if self._buckets[bucket]._state != HashEntry.State.ACTIVE:
            return False
        else:
            self._buckets[bucket]._state = HashEntry.State.DELETED
            self._size -= 1
            return True

    def insert(self,data):
        bucket = self._find_pos(data)
        if self._buckets[bucket]._state == HashEntry.State.ACTIVE:
            return False
        elif self._buckets[bucket]._state == HashEntry.State.EMPTY:
            self._load_size += 1

        self._buckets[bucket]._data = data
        self._buckets[bucket]._state = HashEntry.State.ACTIVE
        self._size += 1
        if self._load_size > self._max_lambda * self._table_size:
            self._rehash()
        return True

    def _rehash(self):
        old_table_size = self._table_size
        self._table_size = self._next_prime(2 * old_table_size)
        old_buckets = copy.copy(self._buckets)
        self._buckets = [HashEntry() for _ in range(self._table_size)]
        self._size = 0
        self._load_size = 0
        for k in range(old_table_size):
            if old_buckets[k]._state == HashEntry.State.ACTIVE:
                self.insert(old_buckets[k]._data)

    def find(self, item):
        bucket = self._find_pos(item)
        bucket_data = self._buckets[bucket]

        if bucket_data._state == HashEntry.State.ACTIVE:
            return bucket_data._data
        else:
            raise HashQP.NotFoundError


def monkey_hash(item):
    if item._sort_by == item.Sort.AUTHOR:
        return hash(item.author)
    if item._sort_by == item.Sort.TITLE:
        return hash(item.title)
    if item._sort_by == item.Sort.SUBJECT:
        return hash(item.subject)
    else:
        return hash(item.ID)


def main():
    eBookEntry.__hash__ = monkey_hash

    # eBookEntry.set_sort_type(eBookEntry.Sort.AUTHOR)
    eBookEntry.set_sort_type(eBookEntry.Sort.ID)

    my_books = eBookEntryReader("catalog-short4.txt")
    my_hash_table = HashQP()

    for book in my_books:
        my_hash_table.insert(book)

    try:
        book = my_hash_table.find(29185)
        # book = my_hash_table.find("Fanny, Aunt, 1822-1894")
        print("Found: ", book.author[0:8],
              book.title[0:10])
    except HashQP.NotFoundError:
        print("Not Found")


    if my_hash_table.remove(29185):
        print("Removed")
    else:
        print("Not Found")

    try:
        book = my_hash_table.find(28493)
        # book = my_hash_table.find("Fanny, Aunt, 1822-1894")
        print("Found: ", book.author[0:8],
              book.title[0:10])
    except HashQP.NotFoundError:
        print("Not Found")


def benchmarking():
    eBookEntry.__hash__ = monkey_hash

    # eBookEntry.set_sort_type(eBookEntry.Sort.AUTHOR)
    eBookEntry.set_sort_type(eBookEntry.Sort.ID)

    my_books = eBookEntryReader("catalog-short4.txt")
    my_hash_table = HashQP()
    bst = BinarySearchTree()
    avl = AVLTree()

    random_ids = random.choices([book.ID for book in my_books], k=10000)
    qp_res = []
    avl_res= []
    bst_res = []

    for book in my_books:
        my_hash_table.insert(book)
        bst.insert(book)
        avl.insert(book)

    qp_time1 = time.time()
    for i in random_ids:
        # print(my_hash_table.find(i))
        book = my_hash_table.find(i)
        qp_res.append(book)
    qp_time2 = time.time()
    print('QP time: ', qp_time2 - qp_time1)

    avl_time1 = time.time()
    for i in random_ids:
        # print(avl.find(i))
        book = avl.find(i)
        avl_res.append(book)
    avl_time2 = time.time()
    print('AVL time: ', avl_time2 - avl_time1)

    bst_time1 = time.time()
    for i in random_ids:
        # print(bst.find(i))
        book = bst.find(i)
        bst_res.append(book)
        # check if all items are same
    bst_time2 = time.time()
    print('BST time: ', bst_time2 - bst_time1)

    # test to see if all the finds were the same
    print(bst_res == avl_res)
    print(bst_res == qp_res)


if __name__ == "__main__":
    benchmarking()
    main()

""" Sample Runs: 
6221 titles loaded
Found:  Fanny, A Baby Night
Not Found
Found:  Fanny, A Baby Night

6221 titles loaded
Found:  Fanny, A Baby Night
Removed
Not Found

Finding different tile then delete and search another:
Found:  United S National S
Removed
Found:  Fanny, A Baby Night


BENCHMARKING RESULTS:
QP time:  0.08826613426208496
AVL time:  0.3981897830963135
BST time:  1.4054210186004639
True
True

The quadratic probing was the fastest, as expected, because the goal of hashing is to have an O(1) time complexity and that seems to be the case. 
AVL is also faster than BST because it is a case of BST that is baslance so the time complexity is usually O(log N) with the divide and conquer methodology. 
BST is the the work of the three because BST is not necessarily balance therefore its runtime at worst is O(N) and best case (if balanced) is O(log N)
although this eBook data most likely isn't O(N), it is probably between O(N) O(log N).  

"""