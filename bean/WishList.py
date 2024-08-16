class Wishlist:
    def __init__(self, wishlist_id, book_title, book_author, genre, is_available):
        self._wishlist_id = wishlist_id
        self._book_title = book_title
        self._book_author = book_author
        self._genre = genre
        self._is_available = is_available

    def get_wishlist_id(self):
        return self._wishlist_id

    def set_wishlist_id(self, value):
        self._wishlist_id = value

    def get_book_title(self):
        return self._book_title

    def set_book_title(self, value):
        self._book_title = value

    def get_book_author(self):
        return self._book_author

    def set_book_author(self, value):
        self._book_author = value

    def get_genre(self):
        return self._genre

    def set_genre(self, value):
        self._genre = value
    def get_is_available(self):
        return self._is_available

    def set_is_available(self, value):
        self._is_available = value
