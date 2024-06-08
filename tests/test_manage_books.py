import io

import pytest
from hamcrest import assert_that, contains_exactly, equal_to, has_items, has_length, is_, none

import manage_books


def test_parse_book_data_one_line():
    one_line = "Isaac Asimov, Prelude to Foundation, Foundation, -2"

    expected_tuple = ("Isaac Asimov", "Prelude to Foundation", "Foundation", -2)

    book_it = manage_books.parse_book_data(io.StringIO(one_line))
    assert_that(next(book_it), is_(equal_to(expected_tuple)))


@pytest.fixture
def foundation_tuples():
    yield [
        ("Isaac Asimov", "Forward the Foundation", "Foundation", -1),
        ("Isaac Asimov", "Foundation", "Foundation", 0),
        ("Isaac Asimov", "Foundation and Empire", "Foundation", 2),
        ("Isaac Asimov", "Second Foundation", "Foundation", 3),
        ("Isaac Asimov", "Foundation's Edge", "Foundation", 4),
        ("Isaac Asimov", "Foundation and Earth", "Foundation", 5),
    ]


@pytest.fixture
def generic_tuples():
    yield [
        ("Author 1", "Title 1", "Series 1", 0),
        ("Author 1", "Title 2", "Series 1", 1),
        ("Author 1", "Title 3", "Series 2", 0),
        ("Author 2", "Title 4", "Series 3", -2),
        ("Author 3", "Title 5", "Series 3", -1),
        ("Author 3", "Title 6", "Series 3", 0),
        ("Author 4", "Title 7", "Series 4", 0),
        ("Author 4", "Title 7", "Series 4", 1),
        ("Author 4", "Title 7", "Series 4", 2),
    ]


def test_parse_book_data_one_multiple_lines(foundation_tuples):
    lines = "\n".join(
        (
            "Isaac Asimov, Forward the Foundation, Foundation, -1",
            "Isaac Asimov, Foundation, Foundation, 0",
            "Isaac Asimov, Foundation and Empire, Foundation, 2",
            "Isaac Asimov, Second Foundation, Foundation, 3",
            "Isaac Asimov, Foundation's Edge, Foundation, 4",
            "Isaac Asimov, Foundation and Earth, Foundation, 5 ",
        )
    )

    book_it = manage_books.parse_book_data(io.StringIO(lines))
    expected_it = iter(foundation_tuples)

    assert_that(next(book_it), is_(equal_to(next(expected_it))))
    assert_that(next(book_it), is_(equal_to(next(expected_it))))
    assert_that(next(book_it), is_(equal_to(next(expected_it))))
    assert_that(next(book_it), is_(equal_to(next(expected_it))))
    assert_that(next(book_it), is_(equal_to(next(expected_it))))
    assert_that(next(book_it), is_(equal_to(next(expected_it))))


def test_get_all_books_by_author(generic_tuples):
    books = generic_tuples

    filtered_books = list(manage_books.get_all_books_by_author(books, "Author 1"))
    assert_that(filtered_books, has_length(3))
    assert_that(filtered_books, has_items(*books[0:3]))

    filtered_books = list(manage_books.get_all_books_by_author(books, "Author 2"))
    assert_that(filtered_books, has_length(1))
    assert_that(filtered_books, has_items(books[3]))

    filtered_books = list(manage_books.get_all_books_by_author(books, "Author 3"))
    assert_that(filtered_books, has_length(2))
    assert_that(filtered_books, has_items(*books[4:6]))

    filtered_books = list(manage_books.get_all_books_by_author(books, "Author 4"))
    assert_that(filtered_books, has_length(3))
    assert_that(filtered_books, has_items(*books[-3:]))

    filtered_books = list(manage_books.get_all_books_by_series(books, "Author 1337"))
    assert_that(filtered_books, has_length(0))


def test_get_all_books_by_series(generic_tuples):
    books = generic_tuples

    filtered_books = list(manage_books.get_all_books_by_series(books, "Series 1"))
    assert_that(filtered_books, has_length(2))
    assert_that(filtered_books, has_items(*books[0:2]))

    filtered_books = list(manage_books.get_all_books_by_series(books, "Series 2"))
    assert_that(filtered_books, has_length(1))
    assert_that(filtered_books, has_items(books[2]))

    filtered_books = list(manage_books.get_all_books_by_series(books, "Series 3"))
    assert_that(filtered_books, has_length(3))
    assert_that(filtered_books, has_items(*books[3:6]))

    filtered_books = list(manage_books.get_all_books_by_series(books, "Series 4"))
    assert_that(filtered_books, has_length(3))
    assert_that(filtered_books, has_items(*books[-3:]))

    filtered_books = list(manage_books.get_all_books_by_series(books, "Series 1337"))
    assert_that(filtered_books, has_length(0))


def test_get_zeroth_book(generic_tuples):
    books = generic_tuples

    book_zero = manage_books.get_zeroth_book(books, "Series 1")
    assert_that(book_zero, equal_to(books[0]))

    book_zero = manage_books.get_zeroth_book(books, "Series 2")
    assert_that(book_zero, equal_to(books[2]))

    book_zero = manage_books.get_zeroth_book(books, "Series 3")
    assert_that(book_zero, equal_to(books[5]))

    book_zero = manage_books.get_zeroth_book(books, "Series 4")
    assert_that(book_zero, equal_to(books[6]))

    book_zero = manage_books.get_zeroth_book(books, "Series 1337")
    assert_that(book_zero, is_(none()))

