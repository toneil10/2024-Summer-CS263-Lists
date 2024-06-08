"""
Collection of utilities used to examine a catalog of books and book series
"""


import csv
import pprint as pp
import sys
from typing import Generator, Iterable, Optional, TextIO


"""
Maximum width for output
"""
WIDTH: int = 80

"""
An 80 character dividing line for use in headings
"""
DIVIDER: str = "-" * WIDTH


"""
Convenient alias for Book-Tuple type hints
"""
BookTuple = tuple[str, str, str, int]


def parse_book_data(src_data: TextIO) -> Generator[BookTuple, None, None]:
    """
    Take a file-like text stream (comma separated) and split it into
    Book-Tuples.

    Args:

        src_data: book data source

    Yields:

        Tuples in the form...

            (author, title, series, # in series)
    """

    csv_reader = csv.reader(src_data)

    for raw_row in csv_reader:
        row = [col.strip() for col in raw_row]
        yield row[0], row[1], row[2], int(row[3])


def get_all_books_by_author(
    books: list[BookTuple], selected_author: str
) -> Iterable[BookTuple]:
    """
    T.B.W
    """

    # Replace the following line
    return []


def get_all_books_by_series(
    books: list[BookTuple], selected_series: str
) -> Iterable[BookTuple]:
    """
    T.B.W
    """

    # Replace the following line
    return []


def get_zeroth_book(
    books: list[BookTuple], selected_series: str
) -> Optional[BookTuple]:
    """
    T.B.W
    """


    # return None if no such book exists
    return None


def main():
    """
    Command line arguments are optional. If not filename is provided... default
    to 'books-0.txt'
    """

    try:
        book_filename = sys.argv[1]

    except IndexError as _err:
        book_filename = "books-0.txt"

    with open(book_filename) as book_file:
        books = list(parse_book_data(book_file))

    title = "Full Book List"
    print(f"{DIVIDER}\n{title:^{WIDTH}}\n{DIVIDER}")
    pp.pprint(books)
    print()

    title = "Books by Isaac Asimov"
    print(f"{DIVIDER}\n{title:^{WIDTH}}\n{DIVIDER}")
    filtered_books = list(get_all_books_by_author(books, "Isaac Asimov"))
    pp.pprint(filtered_books)
    print()

    title = "Books in the Foundation series"
    print(f"{DIVIDER}\n{title:^{WIDTH}}\n{DIVIDER}")
    filtered_books = list(get_all_books_by_series(books, "Foundation"))
    pp.pprint(filtered_books)
    print()

    title = "Book 'Zero' in the Foundation series"
    print(f"{DIVIDER}\n{title:^{WIDTH}}\n{DIVIDER}")
    book_zero = get_zeroth_book(books, "Foundation")
    pp.pprint(book_zero)
    print()

    title = "Books in the Dune series"
    print(f"{DIVIDER}\n{title:^{WIDTH}}\n{DIVIDER}")
    filtered_books = list(get_all_books_by_series(books, "Dune"))
    pp.pprint(filtered_books)
    print()

    title = "Book 'Zero' in the Dune series"
    print(f"{DIVIDER}\n{title:^{WIDTH}}\n{DIVIDER}")
    book_zero = get_zeroth_book(books, "Dune")
    pp.pprint(book_zero)
    print()


if __name__ == "__main__":
    main()
