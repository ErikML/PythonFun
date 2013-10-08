'''
largest_sum_less_than_M

Code by Erik Lindgren

This is problem 3 for the Start @ a Startup Programming contest on HackerRank

Code Description:
Given a set of numbers d and an integer k, finds the largest number that
is a sum of k numbers in d and less than M. It will also output the possible 
ways that this number can be written as a sum, the number of partitions

Problem Statement:
You are given n positive integers: d[0], d[1], ..., d[n-1] and k and M.

Task 1: Choose k numbers from the n integers and output Z, the largest sum of 
the chosen numbers strictly lower than M. 
Formally S = d[p[0]] + d[p[1]] + ... + d[p[k-1]], Z = max{S | S < M}

Task 2: Output P(Z), the number of possible partitions of Z. 
Since P(Z) can be large, output it modulo 1000000007.

Input Format:
n k M
d[0] d[1] ... d[n - 1]

Example Test Case (copy and paste as input):
67 54 2987
17 65 65 72 63 19 38 83 44 88 32 15 17 67 24 94 93 25 44 81 55 4 72 40 34 7 81 90 79 36 78 4 67 45 4 77 27 69 85 51 30 15 94 95 84 68 40 16 28 77 71 49 70 60 45 82 60 3 15 78 42 45 76 15 24 54 73
'''
import time
def main():
    print 'Enter input:'
    [n, k, M] = map(int, raw_input().split())
    d = map(int, raw_input().split())
    start = time.time()
    z = get_largest_sum(d, n, k, M)
    mid = time.time()
    print 'Z:', z
    print 'Calculated in', mid - start, 's'
    print 'P(Z):', get_partitions(z) % 1000000007
    print 'Calculated in', time.time() - mid, 's'
    
def get_largest_sum(d, n, k, M):
    
    """ This is a variant of the 1-0 knapsack problem. The addition is to make
    the number of items exactly k. This is solved by making the lookup return
    -inf when a list is emptied before k items are removed. Using dynamic
    programming the program can run in pseudo-polynomial time
    """
    # NumPy vector would have been better but the contest did not allow
    # outside code so using Python list of list
    lookup_table = [[[0] * (k + 1) for _ in xrange(M)] for _ in xrange(n + 1)]
    # All values now correct when i, j, or l are 0
    for j in xrange(M):
        for l in xrange(k + 1):
            if l != 0:
                # If the list finished but k != 0 (indicator of a 
                # finished list) then return -inf to make it impossible to be a
                # set with less than k elements
                lookup_table[0][j][l] = -float('inf')

    # Modification of dynamic programming algorithm found on wikipedia page
    # for the knapsack problem
    for i in xrange(1, n + 1):
        for j in xrange(1,M):
            for l in xrange(1,k + 1):
                if j >= d[i - 1] and l >= 1:
                    lookup_table[i][j][l] = max(
                            lookup_table[i - 1][j][l],
                            lookup_table[i - 1][j - d[i - 1]][l - 1] + d[i - 1]
                                                )
                else:
                    lookup_table[i][j][l] = lookup_table[i - 1][j][l]   
    return lookup_table[n][M - 1][k]

def get_partitions(Z):
    """ Finds the number of partitions of Z by using an equation by Euler. This
    program calculates the number of partitions of all numbers less than Z and
    saves the data in a lookup table to speed up calculations and prevent
    stack overflows.
    """
    lookup_table = [0 for _ in xrange(Z + 1)]
    lookup_table[0] = 1
    lookup_table[1] = 1
    
    # Build the table
    for m in xrange(2, Z + 1):
        if lookup_table[m] != 0:
            continue
        for k in xrange(1, m + 1):
            # Equation by Euler
            # Found on partitions Wolfram MathWorld Partition Function page
            A = m - k * (3 * k - 1) // 2
            if A < 0:
                A = 0
            else:
                A = lookup_table[A]
            B = m - k * (3 * k + 1) // 2
            if B < 0:
                B = 0
            else:
                B = lookup_table[B] 
            lookup_table[m] += ((-1)**(k + 1) * (A + B))
    return lookup_table[Z]

if __name__ == '__main__':
    main()