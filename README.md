# GROUP 1 - Lab 1 - Unrolled Linked List

## Description

This project contains a mutable implementation of an unrolled linked list
for Lab 1 of the Computational Process Organization course.

## Project Structure

- `unrolled_linked_list.py` - implementation of the mutable unrolled linked
  list
- `unrolled_linked_list_test.py` - unit tests and property-based tests
- `requirements.txt` - project dependency list
- `README.md` - project description and notes

## Contribution

- Pan Yuehao - implementation, testing, and documentation
- Pan Xuanting - lab requirements check, summarize

## Features

- Mutable unrolled linked list implementation
- Configurable node size
- Support for `None` values
- Index-based `get`, `set`, and `remove`
- `add`, `size`, `member`, and `reverse`
- `from_list` and `to_list`
- `filter`, `map`, and `reduce`
- `empty` and `concat`
- Iterator support
- Equality and string representation
- Unit tests
- Property-based tests with Hypothesis

## Changelog

- Initial project setup from course template
- Added mutable unrolled linked list implementation
- Added unit tests and property-based tests
- Updated README

## Design Note

This project implements Lab 1 in mutable style, so operations modify the
current object in place whenever applicable.

The internal representation is a linked list of nodes. Each node stores a
chunk of elements in a Python built-in list.

The node size is configurable through the constructor.

This implementation supports `None` as a valid stored value.

Index-based operations are implemented for `get` and `set`. In this
implementation, `remove` deletes an element by index.

Two lists are considered equal if they contain the same values in the same
order. Internal chunk layout is treated as an implementation detail.

