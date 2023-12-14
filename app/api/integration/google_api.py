import requests
from typing import List, Optional
from app.models.models import Book
from app.api.books.schemas import BookOut
from sqlalchemy import DateTime
from datetime import datetime
from app.api.common.env_manager import EnvManager

class GoogleBooksIntegration:
    GOOGLE_BOOKS_API_URL = EnvManager.GOOGLE_BOOKS_API_URL

    @classmethod
    async def search_books(cls, query: str) -> Optional[List[BookOut]]:
        params = {'q': query}
        response = requests.get(cls.GOOGLE_BOOKS_API_URL, params=params)

        if response.status_code == 200:
            items = response.json().get('items', [])
            books = [cls._convert_google_book_to_model(item) for item in items]
            return books
        else:
            return None

    @classmethod
    async def get_book_info(cls, book_id: str):
        # Make the request to the Google Books API to get the book information by book ID
        url = f"{cls.GOOGLE_BOOKS_API_URL}/{book_id}"
        response = requests.get(url)
        
        if response.status_code == 200:
            book = response.json()

            book_data = cls._convert_google_book_to_model(book, True)
            del book_data['source']

            return book_data
        else:
            return None

    @staticmethod
    def _convert_google_book_to_model(item, to_created:bool=False) -> BookOut:
        volume_info = item.get('volumeInfo', {})
        source_id = item.get('id', '')

        # Map attributes from volume_info to the Book model
        book_data = {
            'title': volume_info.get('title', ''),
            'subtitle': volume_info.get('subtitle', ''),
            'author': ', '.join(volume_info.get('authors', [])),
            'category': ', '.join(volume_info.get('categories', [])),
            'date_publication': volume_info.get('publishedDate', ''),
            'publisher': volume_info.get('publisher', ''),
            'description': volume_info.get('description', ''),
            'image_url': volume_info.get('imageLinks', {}).get('thumbnail', ''),
            'source_id': source_id,
            'source': 'Google',
        }

        # Returns an instance of the Book model
        return BookOut(**book_data) if not to_created else book_data

