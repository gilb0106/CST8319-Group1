
import requests
from bean.Book import Book

def api_query(search_query=None):
    try:
        base_url = "https://www.googleapis.com/books/v1/volumes"
        query_params = "q=publisher:penguin&maxResults=40"

        if search_query:
            encoded_query = requests.utils.quote(search_query)
            query_params = f"q={encoded_query}&maxResults=40"

        url = f"{base_url}?{query_params}"
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        books = []

        if "items" in data:
            for item in data["items"]:
                volume_info = item.get('volumeInfo', {})
                title = volume_info.get('title', 'Unknown')
                authors = volume_info.get('authors', [])
                genre = volume_info.get('categories', [])

                authors_str = ', '.join(authors) if authors else 'Unknown'
                genre_str = ', '.join(genre) if genre else 'Unknown'

                book = Book(0, title, authors_str, genre_str, 0, 0)
                books.append(book)
        else:
            print("No 'items' found in API response.")

        return books

    except requests.RequestException as e:
        print(f"Error fetching books from API: {e}")
        return []

def api_query_startup():
    try:
        response = requests.get("https://www.googleapis.com/books/v1/volumes?q=publisher:penguin&maxResults=5")
        response.raise_for_status()

        data = response.json()
        books = []

        if "items" in data:
            for item in data["items"]:
                volume_info = item.get('volumeInfo', {})
                title = volume_info.get('title', '')
                authors = volume_info.get('authors', [])
                genre = volume_info.get('categories', [])

                authors_str = ', '.join(authors) if authors else ''

                genre_str = ', '.join(genre) if genre else ''

                book = Book(0,title, authors_str, genre_str, 0, 0)
                books.append(book)
        else:
            print("No 'items' found in API response.")

        return books

    except requests.RequestException as e:
        print(f"Error fetching startup books from API: {e}")
        return []