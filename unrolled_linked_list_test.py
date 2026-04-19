import hypothesis.strategies as st
import pytest
from hypothesis import given
from typing import Iterator, TypeVar

from unrolled_linked_list import UnrolledLinkedList

T = TypeVar("T")


def build_list(
    values: list[T],
    node_size: int = 2,
) -> UnrolledLinkedList[T]:
    """Create a list from Python values for testing."""
    lst: UnrolledLinkedList[T] = UnrolledLinkedList(node_size=node_size)
    lst.from_list(values)
    return lst


def test_empty() -> None:
    lst: UnrolledLinkedList[int | None] = UnrolledLinkedList.empty()
    assert lst.to_list() == []
    assert lst.size() == 0
    assert str(lst) == "[]"


def test_invalid_node_size() -> None:
    with pytest.raises(ValueError):
        UnrolledLinkedList(0)

    with pytest.raises(ValueError):
        UnrolledLinkedList(-1)

    with pytest.raises(TypeError):
        UnrolledLinkedList(1.5)  # type: ignore[arg-type]


def test_size() -> None:
    assert UnrolledLinkedList().size() == 0
    assert build_list([1]).size() == 1
    assert build_list([1, 2, 3], node_size=2).size() == 3


def test_to_list() -> None:
    assert UnrolledLinkedList().to_list() == []
    assert build_list([1]).to_list() == [1]
    assert build_list(
        [None, 1, None],
        node_size=2,
    ).to_list() == [None, 1, None]


def test_from_list() -> None:
    test_data: list[list[int | None]] = [
        [],
        [1],
        [1, 2],
        [None, 1, None],
    ]

    for values in test_data:
        lst: UnrolledLinkedList[int | None] = UnrolledLinkedList(
            node_size=2
        )
        lst.from_list(values)
        assert lst.to_list() == values


def test_add() -> None:
    lst: UnrolledLinkedList[int] = UnrolledLinkedList(node_size=2)
    assert lst.to_list() == []

    lst.add(1)
    assert lst.to_list() == [1]

    lst.add(2)
    lst.add(3)
    assert lst.to_list() == [1, 2, 3]


def test_get() -> None:
    lst = build_list([10, 20, 30, 40, 50], node_size=2)

    assert lst.get(0) == 10
    assert lst.get(2) == 30
    assert lst.get(4) == 50


def test_set() -> None:
    lst = build_list([10, 20, 30, 40, 50], node_size=2)

    lst.set(3, 99)

    assert lst.to_list() == [10, 20, 30, 99, 50]


def test_remove() -> None:
    lst = build_list([10, 20, 30, 40, 50], node_size=2)

    lst.remove(1)
    assert lst.to_list() == [10, 30, 40, 50]

    lst.remove(2)
    assert lst.to_list() == [10, 30, 50]


def test_get_set_remove_index_errors() -> None:
    lst = build_list([1, 2, 3], node_size=2)

    with pytest.raises(IndexError):
        lst.get(-1)

    with pytest.raises(IndexError):
        lst.get(3)

    with pytest.raises(IndexError):
        lst.set(10, 5)

    with pytest.raises(IndexError):
        lst.remove(10)

    with pytest.raises(TypeError):
        lst.get("1")  # type: ignore[arg-type]


def test_remove_unlinks_empty_node() -> None:
    lst = build_list([1, 2, 3], node_size=1)

    lst.remove(1)
    assert lst.to_list() == [1, 3]
    assert lst.size() == 2

    lst.remove(0)
    assert lst.to_list() == [3]
    assert lst.size() == 1

    lst.remove(0)
    assert lst.to_list() == []
    assert lst.size() == 0
    assert lst.head is None
    assert lst.tail is None


def test_member() -> None:
    empty: UnrolledLinkedList[int | None] = UnrolledLinkedList()
    lst = build_list([None, 1], node_size=2)

    assert not empty.member(None)
    assert lst.member(None)
    assert lst.member(1)
    assert not lst.member(2)


def test_reverse() -> None:
    lst = build_list([None, 1, 2, 3], node_size=2)

    lst.reverse()

    assert lst.to_list() == [3, 2, 1, None]


def test_map() -> None:
    lst = build_list([1, 2, 3, 4], node_size=2)

    lst.map(lambda x: x * 2)

    assert lst.to_list() == [2, 4, 6, 8]


def test_filter() -> None:
    lst = build_list([1, 2, 3, 4], node_size=2)

    lst.filter(lambda x: x % 2 == 0)

    assert lst.to_list() == [2, 4]


def test_reduce() -> None:
    lst = build_list([1, 2, 3, 4], node_size=2)

    result = lst.reduce(lambda acc, x: acc + x, 0)

    assert result == 10


def test_concat() -> None:
    left = build_list([None, 1], node_size=2)
    right = build_list([1, None], node_size=3)

    left.concat(right)

    assert left.to_list() == [None, 1, 1, None]
    assert right.to_list() == [1, None]


def test_concat_with_self() -> None:
    lst = build_list([1, 2, 3], node_size=2)

    lst.concat(lst)

    assert lst.to_list() == [1, 2, 3, 1, 2, 3]


def test_iter() -> None:
    lst = build_list([None, 1, 2], node_size=2)

    result = []
    for value in lst:
        result.append(value)

    assert result == [None, 1, 2]

    empty_list: UnrolledLinkedList[int | None] = UnrolledLinkedList()
    iterator: Iterator[int | None] = iter(empty_list)
    with pytest.raises(StopIteration):
        next(iterator)


def test_eq_and_str() -> None:
    empty: UnrolledLinkedList[int | None] = UnrolledLinkedList()
    l1 = build_list([None, 1], node_size=2)
    l2 = build_list([None, 1], node_size=3)

    assert str(empty) == "[]"
    assert str(l1) == "[None, 1]"
    assert empty != l1
    assert l1 == l2
    assert l1 != [None, 1]


@given(st.lists(st.one_of(st.none(), st.integers())))
def test_from_list_to_list_equality(values: list[int | None]) -> None:
    lst: UnrolledLinkedList[int | None] = UnrolledLinkedList(node_size=3)
    lst.from_list(values)

    assert lst.to_list() == values


@given(st.lists(st.one_of(st.none(), st.integers())))
def test_python_len_and_list_size_equality(values: list[int | None]) -> None:
    lst: UnrolledLinkedList[int | None] = UnrolledLinkedList(node_size=4)
    lst.from_list(values)

    assert lst.size() == len(values)


@given(st.lists(st.one_of(st.none(), st.integers())))
def test_reverse_twice_restores_original(values: list[int | None]) -> None:
    lst: UnrolledLinkedList[int | None] = UnrolledLinkedList(node_size=3)
    lst.from_list(values)

    lst.reverse()
    lst.reverse()

    assert lst.to_list() == values


@given(st.lists(st.one_of(st.none(), st.integers())))
def test_concat_right_identity(values: list[int | None]) -> None:
    lst: UnrolledLinkedList[int | None] = UnrolledLinkedList(node_size=2)
    empty: UnrolledLinkedList[int | None] = UnrolledLinkedList.empty(
        node_size=5
    )

    lst.from_list(values)
    lst.concat(empty)

    assert lst.to_list() == values


@given(st.lists(st.one_of(st.none(), st.integers())))
def test_concat_left_identity(values: list[int | None]) -> None:
    empty: UnrolledLinkedList[int | None] = UnrolledLinkedList.empty(
        node_size=2
    )
    lst: UnrolledLinkedList[int | None] = UnrolledLinkedList(node_size=5)

    lst.from_list(values)
    empty.concat(lst)

    assert empty.to_list() == values
    assert lst.to_list() == values


@given(
    st.lists(st.one_of(st.none(), st.integers())),
    st.lists(st.one_of(st.none(), st.integers())),
    st.lists(st.one_of(st.none(), st.integers())),
)
def test_concat_associativity(
    values_a: list[int | None],
    values_b: list[int | None],
    values_c: list[int | None],
) -> None:
    left: UnrolledLinkedList[int | None] = UnrolledLinkedList(node_size=2)
    left.from_list(values_a)
    left.concat(build_list(values_b, node_size=3))
    left.concat(build_list(values_c, node_size=4))

    right: UnrolledLinkedList[int | None] = UnrolledLinkedList(node_size=2)
    right.from_list(values_a)
    middle = build_list(values_b, node_size=3)
    middle.concat(build_list(values_c, node_size=4))
    right.concat(middle)

    assert left.to_list() == right.to_list()
