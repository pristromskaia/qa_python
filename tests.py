import pytest
from main import BooksCollector
from books_data import (CHILDREN_BOOKS, ADULT_BOOKS, BOOK_WITHOUT_GENRE)

class TestBooksCollector:
    
    # пример теста:
    def test_add_new_book_add_two_books(self):
        collector = BooksCollector()

        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        assert len(collector.get_books_genre()) == 2

    # добавление новой книги
    def test_add_new_book_adds_book(self, collector):
        collector.add_new_book("Дюна")
        
        assert "Дюна" in collector.get_books_genre()
        
    # проверка на добавление дубликата книги
    def test_add_new_book_ignore_duplicate_book(self):
        collector = BooksCollector()

        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Гордость и предубеждение и зомби')

        assert len(collector.get_books_genre()) == 1

    # проверка на добавление книги с некорректным именем
    @pytest.mark.parametrize("name", ["", "A" * 41])
    def test_add_new_book_invalid_name_not_added(self, collector, name):
        collector.add_new_book(name)
        
        assert name not in collector.get_books_genre()

    # проверка, что у добавленной книги жанр по умолчанию пустой
    def test_added_book_has_empty_genre(self, collector):
        collector.add_new_book("Книга без жанра")
        
        assert collector.get_book_genre("Книга без жанра") == ""
        
    # установить жанр книги
    def test_set_book_genre_sets_correct_genre(self, collector):
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", "Фантастика")
        
        assert collector.get_book_genre("Книга") == "Фантастика"

    # проверка, что не устанавливается несуществующий жанр
    def test_set_book_genre_invalid_genre_not_set(self, collector):
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", "Роман")
        
        assert collector.get_book_genre("Книга") == ""

    # получить книги с определенным жанром
    @pytest.mark.parametrize(
        "genre, expected_books",
        [
            ("Фантастика", ["Гарри Поттер"]),
            ("Ужасы", ["Оно"]),
            ("Детективы", ["Шерлок Холмс"]),
        ],
    )
    def test_get_books_with_specific_genre(self, collector_with_genres, genre, expected_books):
        assert collector_with_genres.get_books_with_specific_genre(genre) == expected_books
        
    # получить книги для детей
    def test_get_books_for_children_returns_only_children_books(self, collector_with_genres):
        result = collector_with_genres.get_books_for_children()
        
        assert sorted(result) == sorted(CHILDREN_BOOKS)
        
    # проверка, что в книги для детей не попадают книги с возрастным рейтингом
    def test_get_books_for_children_excludes_adult_books(self, collector_with_genres):
        result = collector_with_genres.get_books_for_children()
        
        for book in ADULT_BOOKS:
            assert book not in result
            
    # проверка, что в книги для детей не попадают книги без жанра
    def test_get_books_for_children_excludes_books_without_genre(self, collector_with_genres):
        assert BOOK_WITHOUT_GENRE not in collector_with_genres.get_books_for_children()

    # добавление книги в Избранное
    def test_add_book_to_favorites(self, collector_with_genres):
        collector_with_genres.add_book_in_favorites("Гарри Поттер")
        
        assert collector_with_genres.get_list_of_favorites_books() == ["Гарри Поттер"]
        
    # проверка, что книга добавляется в Избранное только один раз
    def test_add_book_to_favorites_only_once(self, collector_with_genres):
        collector_with_genres.add_book_in_favorites("Гарри Поттер")
        collector_with_genres.add_book_in_favorites("Гарри Поттер")
        
        assert collector_with_genres.get_list_of_favorites_books() == ["Гарри Поттер"]
    
    # проверка, что в Избранное не добавляется книга, отсутствующая в books_genre
    def test_add_book_in_favorites_does_not_add_book_not_in_books_genre(self, collector):
        collector.add_book_in_favorites("Неизвестная книга")

        assert collector.get_list_of_favorites_books() == []
 
    # удаление книги из Избранного
    def test_delete_book_from_favorites(self, collector_with_genres):
        collector_with_genres.add_book_in_favorites("Гарри Поттер")
        collector_with_genres.delete_book_from_favorites("Гарри Поттер")
        assert collector_with_genres.get_list_of_favorites_books() == []
        