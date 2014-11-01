import operator as op
from heaps import heapify_raw, sift_down
from binary_trees import BinarySearchTree

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

def mergesort_merge(left_array, right_array, comp):
    # merge two arrays according to the mergesort method
    merged_array = []
    while len(left_array) > 0 or len(right_array) > 0:
        if len(left_array) > 0 and len(right_array) > 0:
            if comp(left_array[0], right_array[0]):
                merged_array.append(left_array.pop(0))
            else:
                merged_array.append(right_array.pop(0))
        elif len(left_array) > 0:
            merged_array.append(left_array.pop(0))
        elif len(right_array) > 0:
            merged_array.append(right_array.pop(0))
    return merged_array

def mergesort_raw(array, comp):
    # sort an array using the quicksort algorithm, returning a sorted array
    if len(array) <= 1:
        return array
    middle = len(array) // 2
    left_array = mergesort_raw(array[:middle], comp)
    right_array = mergesort_raw(array[middle:], comp)
    return mergesort_merge(left_array, right_array, comp)

def mergesort(array, reverse=False):
    # sort an array using the quicksort algorithm, returning a sorted array
    comp = op.gt if reverse else op.lt
    return mergesort_raw(array, comp)

def treesort(array, reverse=False):
    # sort an array using a binary tree insertion algorithm
    comp = op.gt if reverse else op.lt
    tree = BinarySearchTree(comp)
    for elem in array:
        tree.insert(elem)
    return list(map(lambda n: n.key, tree.in_order_traversal()))
