import operator as op

def sift_up(array, comp, start, end):
    child = end
    while child > start:
        parent = int((child - 1) / 2)
        if comp(array[child], array[parent]):
            array[parent], array[child] = array[child], array[parent]
            child = parent
        else:
            break

def sift_down(array, comp, start, end):
    root = start
    while root * 2 + 1 <= end:
        child = root * 2 + 1
        swap = root
        if comp(array[child], array[swap]):
            swap = child
        if child + 1 <= end and comp(array[child + 1], array[swap]):
            swap = child + 1
        if swap != root:
            array[root], array[swap] = array[swap], array[root]
            root = swap
        else:
            break

def heapify_raw(array, comp, method):
    if method == 'down':
        end = len(array) - 1
        for start in range(int(len(array) - 2 / 2), -1, -1):
            sift_down(array, comp, start, end)
    else:
        start = 0
        for end in range(1, len(array)):
            sift_up(array, comp, start, end)

def heapify(array, type='max', method='down'):
    # heapify an array in place
    if type not in ('max', 'min'):
        raise ValueError('comp should be one of (max, min)')
    comp = op.lt if type == 'min' else op.gt
    if method not in ('up', 'down'):
        raise ValueError('method should be one of (up, down)')
    heapify_raw(array, comp, method)
