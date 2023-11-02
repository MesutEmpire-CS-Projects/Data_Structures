import unittest

from Treap.treap import Treap


class TestTreapMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.my_treap = Treap()
        self.my_treap.insert(10)
        self.my_treap.insert(20)
        self.my_treap.insert(30)
        self.my_treap.insert(40)
        self.my_treap.insert(50)
        self.my_treap.insert(60)
        self.my_treap.insert(70)

    def test_len(self):
        self.assertEqual(len(self.my_treap), 7)

    def test_iterator(self):
        my_nums = [10, 20, 30, 40, 50, 60]
        my_nums_sorted = sorted([10, 20, 30, 40, 50, 60])
        my_treap = Treap()

        for num in my_nums:
            my_treap.insert(num)

        i = 0
        for num in my_treap:
            with self.subTest(i=i):
                self.assertEqual(num, my_nums_sorted[i])
                i += 1

    def test_split(self):
        left_treap, right_treap = self.my_treap.split(40)
        self.assertIsNotNone(left_treap)
        self.assertIsNotNone(right_treap)
        self.assertTrue(len(left_treap), 4)
        self.assertTrue(len(right_treap), 3)

    def test_merge(self):
        left_treap, right_treap = self.my_treap.split(40)
        merged_treap = Treap.merge(left_treap, right_treap)
        self.assertEqual(len(merged_treap), len(left_treap) + len(right_treap))


if __name__ == '__main__':
    unittest.main()
