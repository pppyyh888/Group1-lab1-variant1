import hypothesis.strategies as st
import pytest
from hypothesis import given

from unrolled_linked_list import UnrolledLinkedList


def test_empty() -> None:
    lst = UnrolledLinkedList.empty()
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


def test_add_and_to_list() -> None:
    lst = UnrolledLinkedList(node_size=2)
    assert lst.to_list() == []

    lst.add("a")
    assert lst.to_list() == ["a"]

    lst.add("b")
    lst.add("c")
    assert lst.to_list() == ["a", "b", "c"]


def test_from_list() -> None:
    test_data: list[list[int | None]] = [
        [],
        [1],
        [1, 2],
        [None, 1, None],
    ]

    for values in test_data:
        lst = UnrolledLinkedList(node_size=2)
        lst.from_list(values)
        assert lst.to_list() == values


def test_get_set_remove_across_chunks() -> None:
    lst = UnrolledLinkedList(node_size=2)
    lst.from_list([10, 20, 30, 40, 50])

    assert lst.get(0) == 10
    assert lst.get(2) == 30
    assert lst.get(4) == 50

    lst.set(3, 99)
    assert lst.to_list() == [10, 20, 30, 99, 50]

    lst.remove(1)
    assert lst.to_list() == [10, 30, 99, 50]

    lst.remove(2)
    assert lst.to_list() == [10, 30, 50]


def test_get_set_remove_index_errors() -> None:
    lst = UnrolledLinkedList(node_size=2)
    lst.from_list([1, 2, 3])

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
    lst = UnrolledLinkedList(node_size=1)
    lst.from_list([1, 2, 3])

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


def test_member_with_none() -> None:
    empty = UnrolledLinkedList()
    lst = UnrolledLinkedList()
    lst.from_list([None, 1])

    assert not empty.member(None)
    assert lst.member(None)
    assert lst.member(1)
    assert not lst.member(2)


def test_reverse() -> None:
    lst = UnrolledLinkedList(node_size=2)
    lst.from_list([None, 1, 2, 3])

    lst.reverse()
    assert lst.to_list() == [3, 2, 1, None]


def test_map_filter_and_reduce() -> None:
    lst = UnrolledLinkedList(node_size=2)
    lst.from_list([1, 2, 3, 4])

    lst.map(lambda x: x * 2)
    assert lst.to_list() == [2, 4, 6, 8]

    lst.filter(lambda x: x % 4 == 0)
    assert lst.to_list() == [4, 8]

    result = lst.reduce(lambda acc, x: acc + x, 0)
    assert result == 12


def test_concat() -> None:
    left = UnrolledLinkedList(node_size=2)
    right = UnrolledLinkedList(node_size=3)
    left.from_list([None, 1])
    right.from_list([1, None])

    left.concat(right)
    assert left.to_list() == [None, 1, 1, None]
    assert right.to_list() == [1, None]


def test_concat_with_self() -> None:
    lst = UnrolledLinkedList(node_size=2)
    lst.from_list([1, 2, 3])

    lst.concat(lst)
    assert lst.to_list() == [1, 2, 3, 1, 2, 3]


def test_iter() -> None:
    lst = UnrolledLinkedList(node_size=2)
    lst.from_list([None, 1, 2])

    result = []
    for value in lst:
        result.append(value)

    assert result == [None, 1, 2]

    iterator = iter(UnrolledLinkedList())
    with pytest.raises(StopIteration):
        next(iterator)


def test_eq_and_str() -> None:
    empty = UnrolledLinkedList()
    l1 = UnrolledLinkedList(node_size=2)
    l2 = UnrolledLinkedList(node_size=3)

    l1.from_list([None, 1])
    l2.from_list([None, 1])

    assert str(empty) == "[]"
    assert str(l1) == "[None, 1]"
    assert empty != l1
    assert l1 == l2
    assert l1 != [None, 1]


@given(st.lists(st.one_of(st.none(), st.integers())))
def test_from_list_to_list_roundtrip(values: list[int | None]) -> None:
    lst = UnrolledLinkedList(node_size=3)
    lst.from_list(values)
    assert lst.to_list() == values


@given(st.lists(st.one_of(st.none(), st.integers())))
def test_python_len_and_list_size_equality(values: list[int | None]) -> None:
    lst = UnrolledLinkedList(node_size=4)
    lst.from_list(values)
    assert lst.size() == len(values)


@given(st.lists(st.one_of(st.none(), st.integers())))
def test_reverse_twice_restores_original(values: list[int | None]) -> None:
    lst = UnrolledLinkedList(node_size=3)
    lst.from_list(values)

    lst.reverse()
    lst.reverse()

    assert lst.to_list() == values


@given(st.lists(st.one_of(st.none(), st.integers())))
def test_member_matches_python_in(values: list[int | None]) -> None:
    lst = UnrolledLinkedList(node_size=2)
    lst.from_list(values)

    assert lst.member(None) == (None in values)

    if values:
        assert lst.member(values[0])


@given(st.lists(st.one_of(st.none(), st.integers())))
def test_concat_with_empty_preserves_values(values: list[int | None]) -> None:
    lst = UnrolledLinkedList(node_size=2)
    empty = UnrolledLinkedList.empty(node_size=5)

    lst.from_list(values)
    lst.concat(empty)

    assert lst.to_list() == values
