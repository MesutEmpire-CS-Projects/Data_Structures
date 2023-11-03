from typing import Generic, TypeVar, Self

T = TypeVar("T")


class _StackNode(Generic[T]):
    def __init__(self, element: T):
        self.element = element
        self.next: Self | None = None


class Stack(Generic[T]):
    """
    This is a software stack that stores _elements in LIFO.
    Generics were added purely for type hinting; assuming that items of the
    same type will be stored in the stack.
    The Python interpreter, however, does not enforce this at runtime.
    """

    class EmptyStackException(Exception):
        def __init__(self):
            super().__init__("Stack is empty")

    def __init__(self):
        self._head: _StackNode | None = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self):
        """Returns `True` if the stack has no _elements"""
        return len(self) == 0

    def push(self, element: T) -> None:
        """Adds an element to the top of the stack"""
        new_node = _StackNode(element)
        current_head = self._head
        new_node.next = current_head
        self._head = new_node

        self._size += 1

    def pop(self) -> T:
        """
        Removes and returns the element at the top of the stack
        :raise: EmptyStackException
        """
        if self.is_empty():
            raise Stack.EmptyStackException()

        element = self._head.element
        previous_head = self._head
        self._head = previous_head.next
        previous_head.next = None
        previous_head.data = None
        self._size -= 1

        return element

    def peek(self) -> T:
        """
        Returns (but does not remove) the element at the top of the stack
        :raise: EmptyStackException if the stack is empty
        :return: Element of type T
        """
        if self.is_empty():
            raise Stack.EmptyStackException()
        return self._head.element
