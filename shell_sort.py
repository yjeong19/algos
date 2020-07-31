from tabulate import tabulate
import math
import random
import copy
import time

def shell_sort(target):
    # implied gap sequence
    gap = len(target) // 2
    while gap > 0:
        print(gap)
        for pos in range(gap, len(target)):
            tmp = target[pos]
            k = pos
            while tmp < target[k-gap] and k >= gap:
                target[k] = target[k-gap]
                k -= gap
            target[k] = tmp
        gap //= 2

    return target


def shell_sort_x(target, gap_list):
    gap_list = sorted(gap_list, reverse=True)

    for gap in gap_list:
        print(gap)
        for pos in range(gap, len(target)):
            tmp = target[pos]
            k = pos
            while tmp < target[k - gap] and k >= gap:
                target[k] = target[k - gap]
                k -= gap
            target[k] = tmp

    return target


def insertion_sort(target):
    for pos in range(1, len(target)):
        tmp = target[pos]
        k = pos

        while tmp < target[k - 1] and k > 0:
            target[k] = target[k - 1]
            k -= 1
        target[k] = tmp

    return target


def get_sedgwick_gap(n):
    return_list = [1]
    idx = 0
    curr_max = 0
    while curr_max < n:
        next_gap = 4 ** (idx + 1) + 3 * (2 ** idx) + 1
        if next_gap < n:
            return_list.append(next_gap)
        curr_max = next_gap
        idx += 1
    return return_list


def test_gap_1(n):
    # found this sequence on stack overflow as possibly faster than sedgewick
    return_list = [1]
    curr_max = 1

    while curr_max < n:
        next_gap = math.ceil(curr_max * 2.2)
        if next_gap < n:
            return_list.append(next_gap)
        curr_max = next_gap

    return return_list


def test_shell_sorts(ARRAY_SIZE):
    test_gaps = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024,
                 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288,
                 1048576]

    sedgwick_gap = get_sedgwick_gap(ARRAY_SIZE)
    gap1 = test_gap_1(ARRAY_SIZE)

    # 0 = implicit, 1 = provided gap, 2 = sedgwick, 3 = own gap
    results = []


    list_one = list(range(0, ARRAY_SIZE))
    random.shuffle(list_one)
    list_two = copy.copy(list_one)
    list_three = copy.copy(list_one)
    list_four = copy.copy(list_one)
    list_five = copy.copy(list_one)

    print("Implicit Shell Sort...")
    start_time = time.perf_counter()
    a = shell_sort(list_two)
    stop_time = time.perf_counter()
    elapsed = stop_time - start_time
    print("Sorting", ARRAY_SIZE, "items took", elapsed, "seconds")
    results.append(elapsed)

    # testing test gap provided
    print("Explicit sort with test gap provided")
    start_time = time.perf_counter()
    b = shell_sort_x(list_three, test_gaps)
    stop_time = time.perf_counter()
    elapsed = stop_time - start_time
    print("Sorting", ARRAY_SIZE, "items took", elapsed, "seconds")
    results.append(elapsed)

    # test sedgewick
    print('Testing Sedgewick Gap')
    start_time = time.perf_counter()
    c = shell_sort_x(list_four, sedgwick_gap)
    stop_time = time.perf_counter()
    elapsed = stop_time - start_time
    print("Sorting", ARRAY_SIZE, "items took", elapsed, "seconds")
    results.append(elapsed)

    # test own test gap
    print("own test gap sequence")
    start_time = time.perf_counter()
    d = shell_sort_x(list_five, gap1)
    stop_time = time.perf_counter()
    elapsed = stop_time - start_time
    print("Sorting", ARRAY_SIZE, "items took", elapsed, "seconds")
    results.append(elapsed)

    # test if sorted matches.
    print(a == b)
    print(b == c)
    print(c == d)

    return results

a = test_shell_sorts(10000)
b = test_shell_sorts(20000)
c = test_shell_sorts(30000)
d = test_shell_sorts(100000)
e = test_shell_sorts(150000)
f = test_shell_sorts(200000)

table_data = [a, b, c, d, e, f]

headers = ["Implicit", "Provided Gap", "Sedgwick", "Faster than Sedgwick"]
print(tabulate(table_data, headers))

"""
Youngs-MacBook-Pro:cs3c young$ python3 assignment07.py 
Implicit Shell Sort...
5000
2500
1250
625
312
156
78
39
19
9
4
2
1
Sorting 10000 items took 0.061076219 seconds
Explicit sort with test gap provided
1048576
524288
262144
131072
65536
32768
16384
8192
4096
2048
1024
512
256
128
64
32
16
8
4
2
1
Sorting 10000 items took 0.146982676 seconds
Testing Sedgewick Gap
4193
1073
281
77
23
8
1
Sorting 10000 items took 0.05829227100000001 seconds
own test gap sequence
9095
4134
1879
854
388
176
80
36
16
7
3
1
Sorting 10000 items took 0.04863028199999997 seconds
True
True
True
Implicit Shell Sort...
10000
5000
2500
1250
625
312
156
78
39
19
9
4
2
1
Sorting 20000 items took 0.143098534 seconds
Explicit sort with test gap provided
1048576
524288
262144
131072
65536
32768
16384
8192
4096
2048
1024
512
256
128
64
32
16
8
4
2
1
Sorting 20000 items took 0.42288187499999996 seconds
Testing Sedgewick Gap
16577
4193
1073
281
77
23
8
1
Sorting 20000 items took 0.11942370400000002 seconds
own test gap sequence
9095
4134
1879
854
388
176
80
36
16
7
3
1
Sorting 20000 items took 0.10749143699999997 seconds
True
True
True
Implicit Shell Sort...
15000
7500
3750
1875
937
468
234
117
58
29
14
7
3
1
Sorting 30000 items took 0.22698195899999996 seconds
Explicit sort with test gap provided
1048576
524288
262144
131072
65536
32768
16384
8192
4096
2048
1024
512
256
128
64
32
16
8
4
2
1
Sorting 30000 items took 0.7482030300000002 seconds
Testing Sedgewick Gap
16577
4193
1073
281
77
23
8
1
Sorting 30000 items took 0.1918521099999997 seconds
own test gap sequence
20009
9095
4134
1879
854
388
176
80
36
16
7
3
1
Sorting 30000 items took 0.16976505399999997 seconds
True
True
True
Implicit Shell Sort...
50000
25000
12500
6250
3125
1562
781
390
195
97
48
24
12
6
3
1
Sorting 100000 items took 1.077719606 seconds
Explicit sort with test gap provided
1048576
524288
262144
131072
65536
32768
16384
8192
4096
2048
1024
512
256
128
64
32
16
8
4
2
1
Sorting 100000 items took 5.538310226999999 seconds
Testing Sedgewick Gap
65921
16577
4193
1073
281
77
23
8
1
Sorting 100000 items took 0.7586046809999996 seconds
own test gap sequence
96845
44020
20009
9095
4134
1879
854
388
176
80
36
16
7
3
1
Sorting 100000 items took 0.6739193869999998 seconds
True
True
True
Implicit Shell Sort...
75000
37500
18750
9375
4687
2343
1171
585
292
146
73
36
18
9
4
2
1
Sorting 150000 items took 1.6501099239999988 seconds
Explicit sort with test gap provided
1048576
524288
262144
131072
65536
32768
16384
8192
4096
2048
1024
512
256
128
64
32
16
8
4
2
1
Sorting 150000 items took 10.684052812000001 seconds
Testing Sedgewick Gap
65921
16577
4193
1073
281
77
23
8
1
Sorting 150000 items took 1.2618819929999994 seconds
own test gap sequence
96845
44020
20009
9095
4134
1879
854
388
176
80
36
16
7
3
1
Sorting 150000 items took 1.0714863940000008 seconds
True
True
True
Implicit Shell Sort...
100000
50000
25000
12500
6250
3125
1562
781
390
195
97
48
24
12
6
3
1
Sorting 200000 items took 2.8105470080000003 seconds
Explicit sort with test gap provided
1048576
524288
262144
131072
65536
32768
16384
8192
4096
2048
1024
512
256
128
64
32
16
8
4
2
1
Sorting 200000 items took 13.577083125000001 seconds
Testing Sedgewick Gap
65921
16577
4193
1073
281
77
23
8
1
Sorting 200000 items took 1.7772263710000047 seconds
own test gap sequence
96845
44020
20009
9095
4134
1879
854
388
176
80
36
16
7
3
1
Sorting 200000 items took 1.4869381070000003 seconds
True
True
True
  Implicit    Provided Gap    Sedgwick    Faster than Sedgwick
----------  --------------  ----------  ----------------------
 0.0610762        0.146983   0.0582923               0.0486303
 0.143099         0.422882   0.119424                0.107491
 0.226982         0.748203   0.191852                0.169765
 1.07772          5.53831    0.758605                0.673919
 1.65011         10.6841     1.26188                 1.07149
 2.81055         13.5771     1.77723                 1.48694


Why does Shell's gap sequence from the modules give a different timing result than the explicit
array described above and passed to shell_sort_x?  Which is faster and why?

The shell sort from the modules ends up being faster because it is dividing by 2 from the giving size of N, whereas
the explicit shell sort always has sorts from 1048576 // 2 down to 1. I think it is slower because it always has those 
gaps regardless of the size of N, therefore there may be some unnecessary sorting done. 

"""