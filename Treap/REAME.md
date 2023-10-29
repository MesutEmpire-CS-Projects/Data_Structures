# TREAP

## 1. Describe a Treap
######  A Treap is a data structure that combines the binary tree and binary heap hence the name Treap ( Tree + Heap ). It stores two values that is : 
  - Key : This follows the Binary Search Tree property where the value to the left is always less than the parent node and the value to the right is always greater than the parent node.
  - Priority : This is a randomly assigned value that follows the Max Heap property where the parent node is always greater than the child node.
###### The key is used to maintain the BST property, ensuring that the elements are ordered, while the priority ensures that the tree maintains the max-heap property, ensuring that higher priority nodes are closer to the root.
    
## 2. Treap Specification

The Treap data structure supports the following operations:

- `insert(key, priority)`: Inserts a new node with the given key and priority while maintaining the BST and max-heap properties.
- `delete(key)`: Deletes the node with the given key, maintaining the BST and max-heap properties.
- `search(key)`: Searches for a node with the given key.
- `inorder()`: Performs an in-order traversal to visit nodes in ascending key order.
- `min()`: Returns the node with the smallest key.
- `max()`: Returns the node with the largest key.
- `split(key)`: Splits the Treap into two Treaps: one with keys less than the given key and one with keys greater or equal to the given key.
- `merge(left, right)`: Merges two Treaps into a single Treap while maintaining the BST and max-heap properties.
- `is_empty()`: Checks if the Treap is empty