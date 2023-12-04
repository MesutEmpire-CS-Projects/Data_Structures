import random

from typing import Self

from stack import Stack

import pandas as pd


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

    # Read the CSV file into a DataFrame
    df = pd.read_csv('C:\\Users\\Ashraf Mohammed\\Desktop\\Computer Science\\ABSTRACT DATA TYPES\\COMPUTERSCIENCE.csv')

    # Extract the "RegNo" values into a list
    student_reg_no = df['RegNo'].tolist()
    duplicate_count = df['RegNo'].duplicated().sum()

    # Print the number of duplicate values
    # print(f"Number of duplicate values in 'RegNo' column: {duplicate_count}")
    # student_reg_no = list(set(student_reg_no))
    # random.shuffle(student_reg_no)
    my_treap = Treap()

    for student in student_reg_no:
        my_treap.insert(student)

    n = int(input("Enter no. of student per groups:"))
    
    grp_name_pos = 1
    student_groups = []
    grp_name = 2
    for reg in my_treap:
        
        student_groups.append(reg)
        group_name = "Group "+str(grp_name)
        if grp_name_pos % n == 0:
            student_groups.append(group_name)
            grp_name += 1
        grp_name_pos += 1

    df["Groups"] = pd.Series(student_groups)
    print("---------------------------")
    print("Groups formed successfully")
    print("------------Overview of the data---------------")
    print(df.head(20))

    print("-------Some facts----------")
    print(f"{my_treap.max().key} was registered the last among his coursemates")
    print(f"{my_treap.min().key} was registered the last among his coursemates")
    
    print("----------Export the data-----------")
    print("Do you wish to export this data to your current dir?(Enter 1:Yes..... any other input is NO)")
    answer = input(">>")
    if answer == 1 or answer == "1":
        df.to_csv('groups.csv', index=False)
        print("DataFrame exported to 'groups.csv'")
    else:
        print("No data was exported...")
    
