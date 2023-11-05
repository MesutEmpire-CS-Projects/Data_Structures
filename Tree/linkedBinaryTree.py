from binaryTree import BinaryTree

class LinkedBinaryTree(BinaryTree):
    """Linked representation of a binary tree structure."""

    class _Node:  # Lightweight, nonpublic class for storing a node.
        __slots__ = '_element', '_parent', '_left', '_right'

        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    class Position(BinaryTree.Position):
        """An abstraction representing the location of a single element."""

        def __init__(self, container, node):
            """Constructor should not be invoked by the user."""
            self._container = container
            self._node = node

        def element(self):
            """Return the element stored at this Position."""
            return self._node._element

        def __eq__(self, other):
            """Return True if other is a Position representing the same location."""
            return type(other) is type(self) and other._node is self._node

    def _validate(self, p):
        """Return associated node if the position is valid."""
        if not isinstance(p, self.Position):
            raise TypeError("p must be a proper Position type")
        if p._container is not self:
            raise ValueError("p does not belong to this container")
        if p._node._parent is p._node:  # convention for deprecated nodes
            raise ValueError("p is no longer valid")
        return p._node

    def _make_position(self, node):
        """Return Position instance for a given node (or None if no node)."""
        return self.Position(self, node) if node is not None else None


    # Binary tree constructor
    def __init__(self):
        """Create an initially empty binary tree."""
        self._root = None
        self._size = 0

    # Public accessors
    def __len__(self):
        """Return the total number of elements in the tree."""
        return self._size

    def root(self):
        """Return the root Position of the tree (or None if the tree is empty)."""
        return self.make_position(self._root)

    def parent(self, p):
        """Return the Position of p's parent (or None if p is the root)."""
        node = self.validate(p)
        return self.make_position(node._parent)

    def left(self, p):
        """Return the Position of p's left child (or None if no left child)."""
        node = self.validate(p)
        return self.make_position(node._left)

    def right(self, p):
        """Return the Position of p's right child (or None if no right child)."""
        node = self.validate(p)
        return self.make_position(node._right)

    def num_children(self, p):
        """Return the number of children of Position p."""
        node = self.validate(p)
        count = 0
        if node._left is not None:
            count += 1
        if node._right is not None:
            count += 1
        return count

    # Nonpublic update methods
    def add_root(self, e):
        """Place element e at the root of an empty tree and return a new Position."""
        if self._root is not None:
            raise ValueError("Root exists")
        self._size = 1
        self._root = self.Node(e)
        return self.make_position(self._root)

    def add_left(self, p, e):
        """Create a new left child for Position p, storing element e."""
        node = self.validate(p)
        if node._left is not None:
            raise ValueError("Left child exists")
        self._size += 1
        node._left = self.Node(e, node)  # node is its parent
        return self.make_position(node._left)

    def add_right(self, p, e):
        """Create a new right child for Position p, storing element e."""
        node = self.validate(p)
        if node._right is not None:
            raise ValueError("Right child exists")
        self._size += 1
        node._right = self.Node(e, node)  # node is its parent
        return self.make_position(node._right)

    def replace(self, p, e):
        """Replace the element at Position p with e and return the old element."""
        node = self.validate(p)
        old = node._element
        node._element = e
        return old

    def delete(self, p):
        """Delete the node at Position p and replace it with its child, if any."""
        node = self.validate(p)
        if self.num_children(p) == 2:
            raise ValueError("Position has two children")
        child = node._left if node._left else node._right
        if child is not None:
            child._parent = node._parent
            if node is self._root:
                self._root = child
            else:
                parent = node._parent
                if node is parent._left:
                    parent._left = child
                else:
                    parent._right = child
            self._size -= 1
            node._parent = node  # convention for deprecated node
        return node._element

    def attach(self, p, t1, t2):
        """Attach trees t1 and t2 as left and right subtrees of external Position p."""
        node = self.validate(p)
        if not self.is_leaf(p):
            raise ValueError("Position must be a leaf")
        if not isinstance(self, type(t1)) or not isinstance(self, type(t2)):
            raise TypeError("Tree types must match")
        self._size += len(t1) + len(t2)
        if not t1.is_empty():
            t1._root._parent = node
            node._left = t1._root
            t1._root = None
            t1._size = 0
        if not t2.is_empty():
            t2._root._parent = node
            node._right = t2._root
            t2._root = None
            t2._size = 0

