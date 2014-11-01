import itertools as it

class BinaryTree(object):
    def __init__(self):
        self.root = None

    def traversal_from(self, node, order):
        """Recursively traverse the given node following the given order.

        This may look a bit complex, but it's actually relatively easy to
        explain: a traversal is the recursive descent unto child nodes, and is
        specifically linked to an order.

        Traversal order is specified as follows:
        0) current node
        1) left child node
        2) right child node

        The order of traversal should therefore be given as an iterable
        specifying what needs to be traversed (example: (0, 1, 2) is the order
        (self, left, right).

        This method is implemented as a generator and yields the nodes (and not
        the  keys), ignoring the nodes that are None.
        """
        if node is None:
            return
        traversal_fns = (lambda: (node),
                         lambda: self.traversal_from(node.left, order),
                         lambda: self.traversal_from(node.right, order))
        yield from it.chain.from_iterable(map(traversal_fns.__getitem__, order))

    def traversal(self, order):
        """Traverse nodes depending on given order of traversal. See
        traversal_from() for details on the order of traversal.
        """
        yield from self.traversal_from(self.root, order)

    def top_down_traversal(self):
        """Traverse the binary tree top-down (eg. parent then children)."""
        yield from self.traversal((0, 1, 2))

    def bottom_up_traversal(self):
        """Traverse the binary tree bottom-up (eg. children then parent)."""
        yield from self.traversal((1, 2, 0))

class BinaryTreeNode(object):
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BinarySearchTree(BinaryTree):
    def search(self, key):
        return self.search_from(key, self.root)

    def search_from(self, key, node):
        if node is None:
            return None
        elif key == node.key:
            return node
        elif key < node.key:
            return self.search(key, node.left)
        else:
            return self.search(key, node.right)

    def in_order_traversal(self, reverse=False):
        yield from self.traversal((1, 0, 2))

    def insert(self, key):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError
