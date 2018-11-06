from binary_trees import BinarySearchTree

def test_root_insertion():
    """Insert a root in an empty tree. The root should be modified."""
    tree = BinarySearchTree()
    tree.insert(42)
    assert tree.root is not None
    assert tree.root.key == 42
    assert tree.root.left is None
    assert tree.root.left is None

def test_simple_insertion():
    """Insert a root node, then two children which should be situated one
    on each side (by inserting in the order middle-smallest-highest).
    """
    tree = BinarySearchTree()
    tree.insert(2, 1, 3)
    assert tree.root.key == 2
    assert tree.root.left.key == 1
    assert tree.root.right.key == 3

def test_increasing_insertion():
    """Insert nodes in increasing order. All the left children should be
    None, and all the right children should have a value (except the leaf).
    These should also be in the order of insertion.
    """
    tree = BinarySearchTree()
    n = 42
    tree.insert(*range(n))

    # root case
    assert tree.root is not None
    assert tree.root.key == 0
    assert tree.root.left is None

    # any other node case
    node = tree.root
    for i in range(1, n):
        node = node.right
        assert node is not None
        assert node.key == i
        assert node.left is None
    assert node.right is None

def test_decreasing_insertion():
    """Insert nodes in decreasing order. All the right children should be
    None, and all the left children should have a value (except the leaf).
    These should also be in the order of insertion.
    """
    tree = BinarySearchTree()
    n = 42
    tree.insert(*reversed(range(n)))

    # root case
    assert tree.root is not None
    assert tree.root.key == n - 1
    assert tree.root.right is None

    # any other node case
    node = tree.root
    for i in range(n - 2, -1, -1):
        node = node.left
        assert node is not None
        assert node.key == i
        assert node.right is None
    assert node.left is None

def test_sample_insertion():
    """Insert nodes in a non particular order. The only verification that
    can be made is on the left and right predicates, ie: all the children
    on the left are smaller that the current, and all those on the right
    are greater or equal than the current.
    """
    tree = BinarySearchTree()
    insertions = [36, 5, 27, 40, 20, 6, 2, 17, 4, 37, 23, 15, 16, 29, 28]
    tree.insert(*insertions)
    def check_node(node, traversed=[]):
        assert node.key not in traversed
        traversed.append(node.key)
        if node.left is not None:
            assert node.left.key < node.key
            check_node(node.left)
        if node.right is not None:
            assert node.key < node.right.key
            check_node(node.right)
        return traversed
    assert tree.root is not None
    traversed = check_node(tree.root)
    assert sorted(traversed) == sorted(insertions)

def test_insertion_return():
    """Insertion should always return the node inserted."""
    insertions = [37, 8, 41, 33, 26, 18, 41, 16, 10, 6, 14, 3, 35, 11, 6]
    tree = BinarySearchTree()
    for i in insertions:
        node = tree.insert(i)
        assert node.key == i

    # multiple insertions should return a list
    tree = BinarySearchTree()
    actual_insertions = map(lambda n: n.key, tree.insert(*insertions))
    assert sorted(insertions) == sorted(actual_insertions)

    # no insertions should raise a ValueError
    try:
        tree.insert()
    except ValueError:
        pass # ok
    except Exception as e:
        assert False, "ValueError should have been raised"
    else:
        assert False, "ValueError should have been raised"
