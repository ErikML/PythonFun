'''
Created on Oct 7, 2013

@author: Erik
'''

import heapq
import itertools

def nth_prime(n):
    prime_generator = endless_sieve_of_erat()
    for _ in xrange(n-1):
        next(prime_generator)
    return next(prime_generator)

def first_n_primes(n):
    prime_generator = endless_sieve_of_erat()
    prime_list = []
    for _ in xrange(n):
        prime_list.append(next(prime_generator))
    return prime_list

def endless_sieve_of_erat():
    """An endless generator that yields primes.
    
    Modified from code by Eric Burnett found on
    http://www.thelowlyprogrammer.com/2010/03/writing-efficient-seive-of-eratosthenes.html
    
    Using the Sieve of Eratosthenes but instead of a boolean array it uses a 
    heap to keep track of the next number to check. It also has an optimization
    to never need to check multiples of 2 and 3.
    
    It works by using a heap so that the next item that is not a prime can
    easily be read by reading the value at the head of the heap.
    """
    
    # The object held in the heap. It has a current value and a way to generate
    # future multiples of the given prime
    class PrimeIterObject(object):
        def __init__(self, prime, future_values):
            self.current_value = prime**2
            self.future_multiples = (prime * i for i in future_values)
        def next(self):
            self.current_value = next(self.future_multiples)
        def __eq__(self, other):
            return self.current_value == other.current_value
        def __ne__(self, other):
            return self.current_value != other.current_value
        def __lt__(self, other):
            return self.current_value < other.current_value
        def __gt__(self, other):
            return self.current_value > other.current_value
        def __le__(self, other):
            return self.current_value <= other.current_value
        def __ge__(self, other):
            return self.current_value >= other.current_value
        
    heap = []
    def inc_heap(heap):
        front = heap[0]
        front.next()
        # Burn current multiple and resort into heap
        heapq.heapreplace(heap, front)
    def future_value_iter(n):
        current_value = n
        # Algorithm to skip multiples of 2 and 3
        cycle = itertools.cycle([2, 4])
        if (n + 1) % 3:
            next(cycle)
        while True:
            yield current_value
            current_value += next(cycle)
    yield 2
    yield 3
    # No need to add PrimeIterObject for 2 and 3 because all multiples removed
    yield 5
    future_checked_values = future_value_iter(7)
    current_value = next(future_checked_values)
    heap.append(PrimeIterObject(5, future_value_iter(5)))
    while True:
        # Skipped all past numbers
        while heap[0].current_value < current_value:
            inc_heap(heap)
        # If a match is found skip to next number
        if heap[0].current_value == current_value:
            inc_heap(heap)
        # Otherwise yield number and add new iterator
        else:
            yield current_value
            it = future_value_iter(current_value)
            next(it)
            heapq.heappush(heap, PrimeIterObject(current_value, it))
        current_value = next(future_checked_values)
        
if __name__ == '__main__':
    n = int(raw_input('Enter n, as in the nth prime number you want:'))
    print nth_prime(n)
    