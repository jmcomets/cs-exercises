import operator as op
import itertools as it

class BinaryTree(object):
    """Simple binary tree, holds the interface for travesal of nodes."""
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
    """Simple binary tree node, having only a left and a right child, as well
    as its key.
    """
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right

class BinaryTreeNodeWithParent(BinaryTreeNode):
    """Binary tree node maintaining a relationship with its parent (using
    therefore more memory).
    """
    def __init__(self, *args, **kwargs):
        """Careful here: properties must be setup before calling super method,
        otherwise the parent logic won't be maintained seamlessly.
        """
        self.parent = None
        self._left = None
        self._right = None
        super().__init__(*args, **kwargs)

    def get_left(self):
        # left getter
        return self._left

    def get_right(self):
        # right getter
        return self._right

    def set_left(self, node):
        # left setter
        if self._left is not None:
            self._left.parent = None
        if node is not None:
            node.parent = self
        self._left = node

    def set_right(self, node):
        # right setter
        if self._right is not None:
            self._right.parent = None
        if node is not None:
            node.parent = self
        self._right = node

    left = property(get_left, set_left, doc='Left child property')
    right = property(get_right, set_right, doc='Right child property')

class BinarySearchTree(BinaryTree):
    """Binary search tree, just list a binary tree, only insertion is
    deterministic due to implicit ordering. Keys are ordered left-to-right,
    using the given comparing function (defaults to "<" operator).

    Edge cases:
        - inserting multiple equal keys inserts multiple nodes
        - deletion of a key which is present more than once only deletes a
          single node, this can be solved either by enforcing the handling of
          multiple keys or forcing the presence of a single equal key (not
          implemented)

    Usage example:
    >>> from binary_trees import BinarySearchTree
    >>> tree = BinarySearchTree()
    >>> tree.insert(4, 2)
    >>> tree.insert(1, 3, 3, 7)
    >>> for node in tree.in_order_traversal():
    ...     print(node.key)
    ...
    1
    2
    3
    3
    4
    7
    """
    def __init__(self, keys=(), comp=op.lt):
        super().__init__()
        self.comp = comp
        for key in keys:
            self.insert(key)

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

    def insert(self, *keys):
        """Insert the given keys in the tree, starting at the root."""
        for key in keys:
            self.root = self.insert_at(key, self.root)

    def _replace_in_parent(self, parent, node, new_node):
        if parent is not None:
            if node == parent.left:
                parent.left = new_node
            elif node == parent.right:
                parent.right = new_node
            else:
                raise ValueError('node to replace should be a direct child')

    def delete_at(self, key, node, parent=None):
        if node is None:
            return
        if key < node.key:
            self.delete_at(key, node.left, node)
        elif key > node.key:
            self.delete_at(key, node.right, node)
        else:
            if node.left is not None and node.right is not None:
                repl, repl_parent = node.right, node
                while repl.left is not None:
                    repl, repl_parent = repl.left, repl
                node.key = repl.key
                self.delete_at(repl.key, repl, repl_parent)
            elif node.left is not None:
                self._replace_in_parent(parent, node, node.left)
            elif node.right is not None:
                self._replace_in_parent(parent, node, node.right)
            else:
                self._replace_in_parent(parent, node, None)

    def delete(self, *keys):
        """Delete the given keys from the tree, starting at the root."""
        for key in keys:
            self.delete_at(key, self.root)

    def min(self, node=None):
        """Returns the node containing the smallest key in the current tree,
        starting at the given node (defaults to the root of the tree).
        """
        if node is None:
            node = self.root
        if node is None:
            return None
        return next(self.in_order_traversal(node))

    def max(self, node=None):
        """Returns the node containing the largest key in the current tree,
        starting at the given node (defaults to the root of the tree).
        """
        if node is None:
            node = self.root
        if node is None:
            return None
        return next(self.in_order_traversal(node, reverse=True))
