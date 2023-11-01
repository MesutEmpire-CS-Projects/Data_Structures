import random

from typing_extensions import Self

from Treap.stack import Stack


class TreapNode:
    def __init__(self, key):
        self.key = key
        self.priority = random.randint(0, 99)
        self.left = None
        self.right = None


class Treap:
    class _TreapIterator:
        def __init__(self, root: TreapNode | None):
            self._stack = Stack[TreapNode]()
            self._traverse_to_min_node(root)

        def __iter__(self):
            return self

        def __next__(self):
            if self._stack.is_empty():
                raise StopIteration
            else:
                node = self._stack.pop()
                key = node.key
                if node.right is not None:
                    self._traverse_to_min_node(node.right)
                return key

        def _traverse_to_min_node(self, root: TreapNode | None):
            if root is not None:
                self._stack.push(root)
                self._traverse_to_min_node(root.left)

    def __init__(self, root: TreapNode | None = None):
        """
        Creates a new Treap.

        The additional optional parameter is used by
        the split and merge methods to create new a Treap
        from a given root node.
        This parameter is not to be filled in by client code
        """
        self.root = root
        if self.root is not None:
            # Calculating the length of a Treap given a root node is as
            # simple as going through traversing through the treap and increasing the
            # count from 0 whenever we find an element
            count = 0
            treap_iterator = self._TreapIterator(root)
            try:
                while True:
                    treap_iterator.__next__()
                    count += 1
            except StopIteration:
                pass
            self._size = count
        else:
            self._size = 0

    def __len__(self):
        return self._size

    def size(self):
        return self._size

    @classmethod
    def _left_rotation(cls, x):
        y = x.right
        t2 = y.left

        y.left = x
        x.right = t2

        return y

    @classmethod
    def _right_rotation(cls, y):
        x = y.left
        t2 = x.right

        x.right = y
        y.left = t2

        return x

    def _insert(self, root, key):
        if root is None:
            root = TreapNode(key)
            self._size += 1
            return root

        if key < root.key:
            root.left = self._insert(root.left, key)
            if root.left.priority > root.priority:
                root = self._right_rotation(root)
        elif key > root.key:
            root.right = self._insert(root.right, key)
            if root.right.priority > root.priority:
                root = self._left_rotation(root)
        else:
            raise Exception('No duplicates allowed')

        return root

    def _delete(self, root, key):
        if root is None:
            return root

        if key < root.key:
            root.left = self._delete(root.left, key)
        elif key > root.key:
            root.right = self._delete(root.right, key)
        else:
            if root.left is None:
                return root.left
            elif root.right is None:
                return root.right

            if root.left.priority > root.right.priority:
                root = self._right_rotation(root)
                root.right = self._delete(root.right, key)
            else:
                root = self._left_rotation(root)
                root.left = self._delete(root.left, key)
        self._size -= 1
        return root

    def split(self, key) -> tuple[Self, Self]:
        left, right = self._split(self.root, key)
        return Treap(left), Treap(right)

    def _split(self, root, key):
        if root is None:
            return None, None

        if key < root.key:
            left, right = self._split(root.left, key)
            root.left = right
            return left, root
        else:
            left, right = self._split(root.right, key)
            root.right = left
            return root, right

    @classmethod
    def merge(cls, left_treap: Self, right_treap: Self) -> Self:
        """
        Takes in two Treaps and merges them into one
        :return: A new Treap containing all the elements of left_treap and right_treap
        """
        merged_root = cls._merge(left_treap.root, right_treap.root)
        return Treap(merged_root)

    @classmethod
    def _merge(cls, left_root: TreapNode | None, right_root: TreapNode | None) -> TreapNode | None:
        """
        Utility method for merging two Treaps given their roots.
        :return: A TreapNode representing the root of the merged Treap.
        """
        if not left_root:
            return right_root
        if not right_root:
            return left_root

        if left_root.priority > right_root.priority:
            left_root.right = cls._merge(left_root.right, right_root)
            return left_root
        else:
            right_root.left = cls._merge(left_root, right_root.left)
            return right_root

    def _search(self, root, key):
        if root is None or root.key == key:
            return root
        if key < root.key:
            return self._search(root.left, key)
        elif key > root.key:
            return self._search(root.right, key)

    @classmethod
    def _min(cls, root):
        while root and root.left:
            root = root.left
        return root

    @classmethod
    def _max(cls, root):
        while root and root.right:
            root = root.right
        return root

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def search(self, key):
        return self._search(self.root, key)

    def min(self):
        return self._min(self.root)

    def max(self):
        return self._max(self.root)

    def inorder(self, root):
        if root:
            self.inorder(root.left)
            print("key:", root.key, "| priority:", root.priority, end="")
            if root.left:
                print(" | left child:", root.left.key, end="")
            if root.right:
                print(" | right child:", root.right.key, end="")
            print()
            self.inorder(root.right)

    def is_empty(self):
        return self.size() == 0

    def __iter__(self):
        return self._TreapIterator(self.root)


if __name__ == "__main__":
    my_treap = Treap()
    my_treap.insert(10)
    my_treap.insert(20)
    my_treap.insert(30)
    my_treap.insert(40)
    my_treap.insert(50)
    my_treap.insert(60)
    my_treap.inorder(my_treap.root)

    left, right = my_treap.split(40)

    print(f"Left : {left.key} and Right: {right.key}")

    data = my_treap.merge(left, right)

    print(f"Data : {data.key}")

    # print(f"{my_treap.search(10)}")
    # print(f"{my_treap.search(20)}")
    # print(f"{my_treap.search(30)}")
    # print(f"{my_treap.search(40)}")
    # print(f"{my_treap.search(50)}")
    # print(f"{my_treap.search(60)}")
    # print(f"{my_treap.search(100)}")
    #
    # print(f"{my_treap.max().key}")
    # print(f"{my_treap.min().key}")
