class Book:
    def __init__(self, book_id, book_name, book_author, genre, branch_id, is_available):
        self._branch_id = branch_id
        self._book_id = book_id
        self._book_name = book_name
        self._book_author = book_author
        self._genre = genre
        self._is_available = is_available

    def get_book_id(self):
        return self._book_id

    def set_book_id(self, book_id):
        self._book_id = book_id

    def get_book_name(self):
        return self._book_name

    def set_book_name(self, book_name):
        self._book_name = book_name

    def get_book_author(self):
        return self._book_author

    def set_book_author(self, book_author):
        self._book_author = book_author

    def get_genre(self):
        return self._genre

    def set_genre(self, genre):
        self._genre = genre

    def get_rating(self):
        return self._rating

    def set_rating(self, rating):
        self._rating = rating

    def get_branch_id(self):
        return self._branch_id

    def set_branch_id(self, branch_id):
        self._branch_id = branch_id

    def get_is_available(self):
        return self._is_available

    def set_is_available(self, is_available):
        self._is_available = is_available
