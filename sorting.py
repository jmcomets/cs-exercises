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

def quicksort_partition(array, comp, start, end):
    # partition an array according to the quicksort method
    pivot = (end + start) // 2
    pivot_value = array[pivot]
    array[pivot], array[end] = array[end], array[pivot]
    index = start
    for i in range(start, end):
        if comp(array[i], pivot_value):
            array[i], array[index] = array[index], array[i]
            index += 1
    array[end], array[index] = array[index], array[end]
    return index

def quicksort_raw(array, comp, start, end):
    # sort an array in place using the quicksort algorithm: implementation
    if start < end:
        pivot = quicksort_partition(array, comp, start, end)
        quicksort_raw(array, comp, start, pivot - 1)
        quicksort_raw(array, comp, pivot + 1, end)

def quicksort(array, reverse=False):
    # sort an array in place using the quicksort algorithm
    comp = op.gt if reverse else op.lt
    quicksort_raw(array, comp, 0, len(array) - 1)
