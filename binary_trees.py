import operator as op
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
        traversal_fns = ((node,),
                         self.traversal_from(node.left, order),
                         self.traversal_from(node.right, order))
        yield from it.chain.from_iterable(map(traversal_fns.__getitem__, order))

    def traversal(self, order, node=None):
        """Traverse nodes depending on given order of traversal. See
        traversal_from() for details on the order of traversal.
        """
        if node is None:
            node = self.root
        yield from self.traversal_from(node, order)

    def top_down_traversal(self, node=None):
        """Traverse the binary tree top-down (eg. parent then children),
        starting at the given node (defaults to the tree's root).
        """
        if node is None:
            node = self.root
        yield from self.traversal((0, 1, 2), node)

    def bottom_up_traversal(self, node=None):
        """Traverse the binary tree bottom-up (eg. children then parent),
        starting at the given node (defaults to the tree's root).
        """
        if node is None:
            node = self.root
        yield from self.traversal((1, 2, 0), node)

class BinaryTreeNode(object):
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = None
        self.right = None

class BinarySearchTree(BinaryTree):
    def __init__(self, comp=op.lt):
        super().__init__()
        self.comp = comp

    def search(self, key):
        """Search for the given key in this tree, returning None if it wasn't
        found. Works on an empty tree.
        """
        return self.search_from(key, self.root)

    def search_from(self, key, node):
        """Search recursively for the given key, starting at the given node.
        Note that if you feel adventurous, you can give a node from another
        tree. Returns None if the key wasn't found, works on a None node.
        """
        if node is None:
            return None
        if self.comp(key, node.key):
            return self.search(key, node.left)
        elif self.comp(node.key, key):
            return self.search(key, node.right)
        else:
            return node

    def in_order_traversal(self, reverse=False, node=None):
        """Traverse the tree in the order that the keys are sorted by, starting
        at the given node (defaults to the tree's root).
        """
        if node is None:
            node = self.root
        yield from self.traversal((2, 0, 1) if reverse else (1, 0, 2), node)

    # pre-order traversal, equivalent to a top-down traversal
    pre_order_traversal = BinaryTree.top_down_traversal

    # post-order traversal, equivalent to a bottom-up traversal
    post_order_traversal = BinaryTree.bottom_up_traversal

    def insert_at(self, key, node):
        """Insert the key recursively from the given node. Note that if you
        feel adventurous, you can give a node from another tree. Returns the
        current node.
        """
        if node is None:
            return BinaryTreeNode(key, None, None)
        if self.comp(key, node.key):
            node.left = self.insert_at(key, node.left)
        else:
            node.right = self.insert_at(key, node.right)
        return node

    def insert(self, key):
        """Insert the given key in the tree, starting at the root of course."""
        self.root = self.insert_at(key, self.root)

    def min(self, node=None):
        """Returns the node containing the smallest key in the current tree,
        starting at the given node (defaults to the root of the tree).
        """
        if node is None:
            node = self.root
        if node is None:
            return None
        return next(self.in_order_traversal())

    def max(self, node=None):
        """Returns the node containing the largest key in the current tree,
        starting at the given node (defaults to the root of the tree).
        """
        if node is None:
            node = self.root
        if node is None:
            return None
        return next(self.in_order_traversal(reverse=True))

    def delete(self, key):
        raise NotImplementedError
