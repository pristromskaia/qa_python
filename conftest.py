import pytest

from main import BooksCollector
from books_data import (
    BOOKS_WITH_GENRES,
    CHILDREN_BOOKS,
    ADULT_BOOKS,
    BOOK_WITHOUT_GENRE,
)


@pytest.fixture
def collector():
    return BooksCollector()


@pytest.fixture
def collector_with_books(collector):
    for book in BOOKS_WITH_GENRES:
        collector.add_new_book(book)
    collector.add_new_book(BOOK_WITHOUT_GENRE)
    return collector


@pytest.fixture
def collector_with_genres(collector_with_books):
    for book, genre in BOOKS_WITH_GENRES.items():
        collector_with_books.set_book_genre(book, genre)
    return collector_with_books
