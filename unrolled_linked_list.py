"""Mutable unrolled linked list implementation for Lab 1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Iterator, Optional


@dataclass
class Node:
    """Store a chunk of values inside the unrolled linked list."""

    values: list[Any] = field(default_factory=list)
    next: Optional["Node"] = None
    prev: Optional["Node"] = None


class UnrolledLinkedList:
    """Mutable unrolled linked list implemented as a linked list of chunks."""

    def __init__(self, node_size: int = 4) -> None:
        self._validate_node_size(node_size)
        self.node_size = node_size
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self._length = 0
        self._iter_node: Optional[Node] = None
        self._iter_index = 0

    @classmethod
    def empty(cls, node_size: int = 4) -> "UnrolledLinkedList":
        """Create an empty list."""
        return cls(node_size=node_size)

    def add(self, value: Any) -> None:
        """Add a new element to the tail of the structure."""
        if self.tail is None:
            node = Node(values=[value])
            self.head = node
            self.tail = node
            self._length = 1
            return

        if len(self.tail.values) < self.node_size:
            self.tail.values.append(value)
            self._length += 1
            return

        node = Node(values=[value], prev=self.tail)
        self.tail.next = node
        self.tail = node
        self._length += 1

    def get(self, index: int) -> Any:
        """Get a value by index."""
        node, offset = self._locate(index)
        return node.values[offset]

    def set(self, index: int, value: Any) -> None:
        """Set a value by index."""
        node, offset = self._locate(index)
        node.values[offset] = value

    def remove(self, index: int) -> None:
        """Remove an element by index."""
        node, offset = self._locate(index)
        del node.values[offset]
        self._length -= 1

        if not node.values:
            self._unlink_node(node)

    def size(self) -> int:
        """Return the number of stored elements."""
        return self._length

    def member(self, value: Any) -> bool:
        """Check whether the value is stored in the structure."""
        current = self.head

        while current is not None:
            if value in current.values:
                return True
            current = current.next

        return False

    def reverse(self) -> None:
        """Reverse the list in place."""
        values = self.to_list()
        values.reverse()
        self.from_list(values)

    def from_list(self, values: list[Any]) -> None:
        """Replace the current structure with values from a Python list."""
        self.head = None
        self.tail = None
        self._length = 0

        for value in values:
            self.add(value)

    def to_list(self) -> list[Any]:
        """Convert the structure to a Python list."""
        result: list[Any] = []
        current = self.head

        while current is not None:
            result.extend(current.values)
            current = current.next

        return result

    def filter(self, predicate: Callable[[Any], bool]) -> None:
        """Keep only values that satisfy the predicate."""
        filtered_values = [
            value for value in self.to_list() if predicate(value)
        ]
        self.from_list(filtered_values)

    def map(self, function: Callable[[Any], Any]) -> None:
        """Apply a function to every value in place."""
        current = self.head

        while current is not None:
            for index, value in enumerate(current.values):
                current.values[index] = function(value)
            current = current.next

    def reduce(
            self,
            function: Callable[[Any, Any], Any],
            initial_state: Any,
    ) -> Any:
        """Reduce all values into a single result."""
        result = initial_state
        current = self.head

        while current is not None:
            for value in current.values:
                result = function(result, value)
            current = current.next

        return result

    def concat(self, other: "UnrolledLinkedList") -> None:
        """Append elements from another list in place."""
        if not isinstance(other, UnrolledLinkedList):
            raise TypeError("other must be an UnrolledLinkedList")

        snapshot = other.to_list()
        for value in snapshot:
            self.add(value)

    def __iter__(self) -> Iterator[Any]:
        """Return the iterator object."""
        self._iter_node = self.head
        self._iter_index = 0
        return self

    def __next__(self) -> Any:
        """Return the next element from the iterator."""
        while self._iter_node is not None:
            if self._iter_index < len(self._iter_node.values):
                value = self._iter_node.values[self._iter_index]
                self._iter_index += 1
                return value

            self._iter_node = self._iter_node.next
            self._iter_index = 0

        raise StopIteration

    def __eq__(self, other: object) -> bool:
        """Check structural equality."""
        if not isinstance(other, UnrolledLinkedList):
            return False

        return self.to_list() == other.to_list()

    def __str__(self) -> str:
        """Return a string representation."""
        return str(self.to_list())

    def _validate_node_size(self, node_size: int) -> None:
        if not isinstance(node_size, int):
            raise TypeError("node_size must be an integer")
        if node_size <= 0:
            raise ValueError("node_size must be greater than zero")

    def _locate(self, index: int) -> tuple[Node, int]:
        if not isinstance(index, int):
            raise TypeError("index must be an integer")
        if index < 0 or index >= self._length:
            raise IndexError("index out of range")

        current = self.head
        remaining = index

        while current is not None:
            if remaining < len(current.values):
                return current, remaining
            remaining -= len(current.values)
            current = current.next

        raise IndexError("index out of range")

    def _unlink_node(self, node: Node) -> None:
        if node.prev is None:
            self.head = node.next
        else:
            node.prev.next = node.next

        if node.next is None:
            self.tail = node.prev
        else:
            node.next.prev = node.prev

        node.next = None
        node.prev = None
