import operator as op
from heaps import heapify_raw, sift_down

def heapsort(array, reverse=False):
    # sort an array in place using the heapsort algorithm
    comp = op.lt if reverse else op.gt
    method = 'down'
    heapify_raw(array, comp, method)
    for end in range(len(array) - 1, -1, -1):
        array[end], array[0] = array[0], array[end]
        sift_down(array, comp, 0, end - 1)
