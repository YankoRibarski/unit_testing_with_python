from project.bookstore import Bookstore
from unittest import TestCase, main


class TestBookstore(TestCase):
    def setUp(self):
        self.store = Bookstore(10)
        self.books = {
            "Javascript book": 2,
            "Python book": 3,
            "C# book": 4
        }

    def test_correct_initialization(self):
        self.assertEqual(10, self.store.books_limit)
        self.assertEqual({}, self.store.availability_in_store_by_book_titles)
        self.assertEqual(0, self.store.total_sold_books)

    def test_invalid_book_limit_raise_ValueError(self):
        with self.assertRaises(ValueError) as ve:
            self.store.books_limit = 0
        self.assertEqual("Books limit of 0 is not valid", str(ve.exception))

    def test_correct_len_method(self):
        self.store.availability_in_store_by_book_titles = self.books
        self.assertEqual(9, len(self.store))

    def test_receive_book_over_limit_raise_exception(self):
        self.store.availability_in_store_by_book_titles = self.books
        with self.assertRaises(Exception) as ex:
            self.store.receive_book("Javascript book", 2)
        self.assertEqual("Books limit is reached. Cannot receive more books!", str(ex.exception))

    def test_receive_book_with_new_book(self):
        result = self.store.receive_book("Program", 1)
        self.assertEqual({"Program": 1}, self.store.availability_in_store_by_book_titles)
        self.assertEqual("1 copies of Program are available in the bookstore.", result)

    def test_receive_book_with_existing_book(self):
        self.store.availability_in_store_by_book_titles = self.books
        result = self.store.receive_book("Python book", 1)
        self.assertEqual("4 copies of Python book are available in the bookstore.", result)

    def test_sell_book_witt_uncorrect_book_raise_exception(self):
        with self.assertRaises(Exception) as ex:
            self.store.sell_book("Program", 1)
        self.assertEqual("Book Program doesn't exist!", str(ex.exception))

    def test_sell_book_with_not_enough_copies(self):
        self.store.availability_in_store_by_book_titles = self.books
        with self.assertRaises(Exception) as ex:
            self.store.sell_book("Javascript book", 3)
        self.assertEqual("Javascript book has not enough copies to sell. Left: 2", str(ex.exception))

    def test_correct_sell_book(self):
        self.store.availability_in_store_by_book_titles = self.books
        result = self.store.sell_book("Javascript book", 2)
        self.assertEqual(self.store.total_sold_books, 2)
        self.assertEqual({'C# book': 4, 'Javascript book': 0, 'Python book': 3
                          }, self.store.availability_in_store_by_book_titles)
        self.assertEqual("Sold 2 copies of Javascript book", result)

    def test_str_method(self):
        self.store.availability_in_store_by_book_titles = self.books
        result = str(self.store)
        self.assertEqual("Total sold books: 0\n"
                         "Current availability: 9\n"
                         " - Javascript book: 2 copies\n"
                         " - Python book: 3 copies\n"
                         " - C# book: 4 copies", result)


if __name__ == '__main__':
    main()
