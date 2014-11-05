import unittest
from binary_trees import BinarySearchTree

class InsertionTest(unittest.TestCase):
    def setUp(self):
        self.tree_class = BinarySearchTree

    def test_root_insertion(self):
        """Insert a root in an empty tree. The root should be modified."""
        tree = self.tree_class()
        tree.insert(42)
        self.assertIsNotNone(tree.root)
        self.assertEqual(tree.root.key, 42)
        self.assertIsNone(tree.root.left)
        self.assertIsNone(tree.root.right)

    def test_simple_insertion(self):
        """Insert a root node, then two children which should be situated one
        on each side (by inserting in the order middle-smallest-highest).
        """
        tree = self.tree_class()
        tree.insert(2, 1, 3)
        self.assertEqual(tree.root.key, 2)
        self.assertEqual(tree.root.left.key, 1)
        self.assertEqual(tree.root.right.key, 3)

    def test_increasing_insertion(self):
        """Insert nodes in increasing order. All the left children should be
        None, and all the right children should have a value (except the leaf).
        These should also be in the order of insertion.
        """
        tree = self.tree_class()
        n = 42
        tree.insert(*range(n))

        # root case
        self.assertIsNotNone(tree.root)
        self.assertEqual(tree.root.key, 0)
        self.assertIsNone(tree.root.left)

        # any other node case
        node = tree.root
        for i in range(1, n):
            node = node.right
            self.assertIsNotNone(node)
            self.assertEqual(node.key, i)
            self.assertIsNone(node.left)
        self.assertIsNone(node.right)

    def test_decreasing_insertion(self):
        """Insert nodes in decreasing order. All the right children should be
        None, and all the left children should have a value (except the leaf).
        These should also be in the order of insertion.
        """
        tree = self.tree_class()
        n = 42
        tree.insert(*reversed(range(n)))

        # root case
        self.assertIsNotNone(tree.root)
        self.assertEqual(tree.root.key, n - 1)
        self.assertIsNone(tree.root.right)

        # any other node case
        node = tree.root
        for i in range(n - 2, -1, -1):
            node = node.left
            self.assertIsNotNone(node)
            self.assertEqual(node.key, i)
            self.assertIsNone(node.right)
        self.assertIsNone(node.left)

    def test_sample_insertion(self):
        """Insert nodes in a non particular order. The only verification that
        can be made is on the left and right predicates, ie: all the children
        on the left are smaller that the current, and all those on the right
        are greater or equal than the current.
        """
        tree = self.tree_class()
        insertions = [36, 5, 27, 40, 20, 6, 2, 17, 4, 37, 23, 15, 16, 29, 28]
        tree.insert(*insertions)
        def check_node(node, traversed=[]):
            self.assertNotIn(node.key, traversed)
            traversed.append(node.key)
            if node.left is not None:
                self.assertTrue(node.left.key < node.key, traversed)
                check_node(node.left)
            if node.right is not None:
                self.assertTrue(node.key < node.right.key, traversed)
                check_node(node.right)
            return traversed
        self.assertIsNotNone(tree.root)
        traversed = check_node(tree.root)
        self.assertEqual(sorted(traversed), sorted(insertions))

    def test_insertion_return(self):
        """Insertion should always return the node inserted."""
        insertions = [37, 8, 41, 33, 26, 18, 41, 16, 10, 6, 14, 3, 35, 11, 6]
        tree = self.tree_class()
        for i in insertions:
            node = tree.insert(i)
            self.assertEqual(node.key, i)

        # multiple insertions should return a list
        tree = self.tree_class()
        actual_insertions = map(lambda n: n.key, tree.insert(*insertions))
        self.assertEqual(sorted(insertions), sorted(actual_insertions))

        # no insertions should raise a ValueError
        with self.assertRaises(ValueError):
            tree.insert()
