""" Young Jeong Assignment 3 Matrix Multiplication """

import random
import time

MAT_SIZE = 100

def multiply_matrices(mat_one, mat_two):
    """
        To multiply an m×n matrix by an n×p matrix, the ns must be the same,
        and the result is an m×p matrix.
    """
    # set 0 for new matrix
    new_mat = [[0 for _ in range(len(mat_two[0]))] for _ in range(len(mat_one))]

    # loop through row in mat_two
    for row in range(len(mat_one)):
        # loop through col in mat_two
        for col in range(len(mat_two[0])):
            # loop through row in mat_two
            for row_2 in range(len(mat_two)):
                new_mat[row][col] += mat_one[row][row_2] * mat_two[row_2][col]
    return new_mat

def show_sub_square(matrix, start, size):
    # Your code here
    end = start + size
    ret_str = ''
    for row in range(start, end):
        for col in range(start, end):
            ret = f'{matrix[row][col] :.2f}'
            ret_str += f'{ret:>8}'
        ret_str += '\n'
    return ret_str



def main():
    # proof of correctness

    mat_one = [[1, 2, 3, 4, 5], [-1, -2, -3, -4, -5],
               [1, 3, 1, 3, 5], [0, 1, 0, 1, 0], [-1, -1, -1, -1, -1]]

    mat_two = [[2, 1, 5, 0, 2], [1, 4, 3, 2, 7],
               [4, 4, 4, 4, 4], [7, 1, -1, -1, -1], [0, 0, 8, -1, -6]]

    print('Test Matrix One: ')
    print(show_sub_square(mat_one, 0, 5))
    print('\nTest Matrix Two')
    print(show_sub_square(mat_two, 0, 5))
    print('Test Product')
    new_mat = multiply_matrices(mat_one, mat_two)
    print(show_sub_square(new_mat, 0, 5))
    print()

    matrix = [[0 for _ in range(MAT_SIZE)] for _ in range(MAT_SIZE)] # Your code - list comprehension to initialize zero matrix

    # generate small fraction of non-default values between 0 and 1
    small_fraction = round(MAT_SIZE * MAT_SIZE * .01)
    for i in range(small_fraction):
        rand_row = random.randrange(MAT_SIZE)
        rand_col = random.randrange(MAT_SIZE)
        matrix[rand_row][rand_col] = random.random()

    print('Matrix to Square: ')
    print(show_sub_square(matrix, MAT_SIZE - 10, 10))

    start_time = time.perf_counter()

    new_mat = multiply_matrices(matrix, matrix)

    stop_time = time.perf_counter()

    elapsed = stop_time - start_time

    print("Product:")
    print(show_sub_square(new_mat, MAT_SIZE - 10, 10))

    print('size: ', MAT_SIZE, "Calculation time:", elapsed, "seconds")

if __name__ == "__main__":
    main()


"""
Part A:
1.  ~160-170 MAT_SIZE was the smallest number to take more than 1 seconds
2. The time it took for the algorithm to complete exponentially grew as size doubled, results of doubling below. 
   size:  10 Calculation time: 0.0003260010000000063 seconds
   size:  20 Calculation time: 0.0023095070000000023 seconds
   size:  40 Calculation time: 0.015814834 seconds
   size:  80 Calculation time: 0.110718761 seconds
   size:  160 Calculation time: 0.9155999549999999 seconds
   size:  320 Calculation time: 7.5448480049999995 seconds
3. When MAT_SIZE was set at 1000, it took over a few minutes. 
4. The data agrees with the time complexity analysis because it looks like it is growing exponentially at about n^3 
   and there are 3 nested loops.
   

Run results:

Test Matrix One: 
    1.00    2.00    3.00    4.00    5.00
   -1.00   -2.00   -3.00   -4.00   -5.00
    1.00    3.00    1.00    3.00    5.00
    0.00    1.00    0.00    1.00    0.00
   -1.00   -1.00   -1.00   -1.00   -1.00


Test Matrix Two
    2.00    1.00    5.00    0.00    2.00
    1.00    4.00    3.00    2.00    7.00
    4.00    4.00    4.00    4.00    4.00
    7.00    1.00   -1.00   -1.00   -1.00
    0.00    0.00    8.00   -1.00   -6.00

Test Product
   44.00   25.00   59.00    7.00   -6.00
  -44.00  -25.00  -59.00   -7.00    6.00
   30.00   20.00   55.00    2.00   -6.00
    8.00    5.00    2.00    1.00    6.00
  -14.00  -10.00  -19.00   -4.00   -6.00


Matrix to Square: 
    0.00    0.00    0.00    0.00    0.00    0.00    0.00    0.00    0.00    0.00
    0.00    0.00    0.00    0.00    0.00    0.00    0.00    0.00    0.00    0.00
    0.00    0.83    0.00    0.37    0.00    0.00    0.00    0.00    0.00    0.00
    0.00    0.00    0.00    0.00    0.00    0.00    0.00    0.00    0.00    0.00
    0.00    0.00    0.99    0.00    0.00    0.00    0.00    0.00    0.00    0.00
    0.00    0.00    0.00    0.00    0.00    0.00    0.89    0.00    0.00    0.00
    0.00    0.16    0.00    0.00    0.00    0.00    0.00    0.00    0.00    0.00
    0.00    0.00    0.00    0.00    0.00    0.00    0.25    0.00    0.00    0.00
    0.00    0.00    0.00    0.00    0.26    0.00    0.00    0.00    0.00    0.64
    0.00    0.00    0.00    0.00    0.00    0.00    0.59    0.00    0.00    0.00

Product:
    0.00    0.00    0.00    0.00    0.03    0.24    0.00    0.55    0.07    0.00
    0.00    0.00    0.00    0.32    0.00    0.17    1.12    0.00    0.40    0.00
    0.27    0.00    0.29    0.29    0.14    0.21    0.35    0.03    0.92    0.00
    0.00    0.77    0.03    0.00    0.00    1.29    0.12    0.12    0.10    0.49
    0.07    0.83    0.03    0.77    0.00    0.82    0.32    0.40    0.11    0.00
    0.01    0.14    0.03    0.08    0.05    0.98    0.27    0.49    0.10    0.00
    0.33    0.51    0.05    0.00    0.00    0.44    0.89    0.03    0.01    0.00
    0.09    0.80    0.12    1.82    0.00    1.06    0.13    0.01    0.27    0.00
    0.00    0.00    0.30    1.17    0.15    0.00    0.54    0.40    0.27    0.00
    1.02    0.39    0.00    0.07    0.00    1.40    0.18    0.00    0.00    0.00

Calculation time: 0.23615562599999998 seconds
"""